#  Copyright (c) 2026. Programacion Cientifica, DISC, Antofagasta, Chile.
import logging
import multiprocessing
from pathlib import Path

from numba import njit
from tqdm import tqdm

from benchmarking import benchmark  # ty:ignore[unresolved-import]
from logger import configure_logging  # ty:ignore[unresolved-import]


@njit(fastmath=True)
def is_prime(num: int) -> bool:
    # Menores que 2 no son primos
    if num < 2:
        return False
    # El 2 y el 3 son primos
    if num == 2 or num == 3:
        return True
    # Múltiplos de 2 o 3 no son primos
    if num % 2 == 0 or num % 3 == 0:
        return False

    # Algoritmo 6k +/- 1 optimizado
    limit = int(num**0.5)
    for i in range(5, limit + 1, 6):
        if num % i == 0 or num % (i + 2) == 0:  # Corregido: comprueba ambos extremos
            return False

    return True


def count_primes_in_range(the_range: tuple[int, int]) -> int:
    primes = 0
    start, end = the_range
    for i in range(start, end):
        if is_prime(i):
            primes += 1
    return primes


def main() -> None:
    n = 10 * 1000 * 1000
    log.debug(f"Counting primes from 1 to {n:,} ..")

    # Configuración de núcleos y bloques (chunks)
    num_cores = 22  # os.cpu_count()
    log.debug(f"num_cores: {num_cores}.")

    # Definimos la granularidad del pipeline multiproceso
    num_chunks = num_cores * 20

    # CORRECCIÓN: El tamaño del chunk debe basarse en num_chunks, no en num_cores
    chunk_size = n // num_chunks

    # Divide de forma exacta el espacio en tuplas (start, end)
    ranges = []
    for i in range(num_chunks):
        start = i * chunk_size
        if i == num_chunks - 1:
            end = n  # Asegura cubrir el residuo decimal hasta N
        else:
            end = (i + 1) * chunk_size
        ranges.append((start, end))

    # Opcional: reducir logs si son demasiados bloques impresos en consola
    log.debug(f"Generated {len(ranges)} work chunks for the pool.")

    # El pool de workers ejecutando el pipeline en paralelo
    with multiprocessing.Pool(num_cores) as pool:
        result = list(
            tqdm(
                pool.imap(count_primes_in_range, ranges),
                total=len(ranges),
                ncols=120,
                desc="Counting primes",
            )
        )

    primes = sum(result)
    log.debug(f"primes: {primes:,}")


# Call the main function
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
