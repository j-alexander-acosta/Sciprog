#  Copyright (c) 2026. Programacion Cientifica, DISC, Antofagasta, Chile.
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from numba import njit
from tqdm import tqdm

from benchmarking import benchmark  # ty:ignore[unresolved-import]
from logger import configure_logging  # ty:ignore[unresolved-import]


# CRITICAL: nogil=True permite que los hilos de Python corran en paralelo real sobre CPU-bound tasks
@njit(fastmath=True, nogil=True)
def is_prime(num: int) -> bool:
    if num < 2:
        return False
    if num == 2 or num == 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False

    # Factorización de salto 6 (Se evalúa i e i+2 para cubrir 6k +/- 1)
    limit = int(num**0.5) + 1
    for i in range(5, limit, 6):
        if num % i == 0 or num % (i + 2) == 0:
            return False
    return True


# Función auxiliar para procesar un rango de números en un solo hilo
@njit(fastmath=True, nogil=True)
def count_primes_in_range(start: int, end: int) -> int:
    count = 0
    for i in range(start, end):
        if is_prime(i):
            count += 1
    return count


def main():
    num = 10 * 100 * 100 * 100  # 10,000,000

    # Detecta automáticamente los hilos lógicos de la CPU (ej. 24 en tu Ryzen)
    max_workers = os.cpu_count() or 4
    log.info(f"Using ThreadPoolExecutor with {max_workers} workers (Numba nogil=True).")

    # Dividir el trabajo en fragmentos (chunks) para que los hilos trabajen en paralelo de forma eficiente
    chunk_size = num // max_workers
    futures = []

    # Inicializamos el ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        log.debug("Submitting chunks to threads...")
        for i in range(max_workers):
            start = i * chunk_size
            # El último chunk absorbe cualquier residuo de la división
            end = num if i == max_workers - 1 else (i + 1) * chunk_size

            # Enviamos la tarea pesada al pool
            futures.append(executor.submit(count_primes_in_range, start, end))

        # Recolectamos los resultados a medida que terminan
        primes = 0
        for future in tqdm(
            futures, total=len(futures), ncols=80, desc="Processing chunks"
        ):
            primes += future.result()

    log.info(f"Found {primes} prime numbers between 1 and {num}.")


if __name__ == "__main__":
    configure_logging(logging.DEBUG)
    log = logging.getLogger(__name__)

    root_dir = Path(__file__).resolve().parent.parent
    log.debug(f"root_dir: {root_dir}")

    output_dir = root_dir / "output"
    log.debug(f"output_dir: {output_dir}")

    with benchmark("main", log):
        log.info("🏎️ starting ..")
        main()
        log.info("🏁 done.")