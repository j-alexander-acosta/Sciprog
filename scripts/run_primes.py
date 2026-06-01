#  Copyright (c) 2026. Programacion Cientifica, DISC, Antofagasta, Chile.
import threading
from concurrent.futures import thread
import logging
import math
from pathlib import Path

from numba import njit
from tqdm import tqdm

from benchmarking import benchmark # ty:ignore[unresolved.ved-import]
from logger import configure_logging # ty:ignore[unresolved-import]

@njit(fastmath=True)
def is_prime(num: int) -> bool:
    # Casos base e inmediatos
    if num < 2:
        return False
    # if exactly 2 true
    if num == 2:
        return True
    # multiple of two or three false
    if num % 2 == 0 or num % 3 == 0:
        return False

    # try all the values
    for i in range (5, int(num ** 0.5) + 1, 6):
        if num % i == 0:
            return False
    return True

def main():
    primes = 0
    num = 10 * 100 * 100 * 100

    threads = []
    log.debug(f"Creating threads ::")
    for i in range(num):
        t = threading.Thread(target=is_prime, args=(num,))
        threads.append(t)

    log.debug(f"Starting threads ::")
    for t in threads:
        t.start()

    log.debug("Waiting for threads ::")
    for t in threads:
        t.join()

    # for i in tqdm(range(num), ncols=0, desc="Finding primes"):
    #         if is_prime(i):
    #            primes += 1
    # log.info(f"found {primes} prime numbers between 1 and {num}.")


# call the main function
if __name__ == "__main__":
    # configure the logging
    configure_logging(logging.DEBUG)
    # get the main logger
    log = logging.getLogger(__name__)

    # get the root directory
    root_dir = Path(__file__).resolve().parent.parent
    log.debug(f"root_dir: {root_dir}")

    # get the output directory
    output_dir = root_dir / "output"
    log.debug(f"output_dir: {output_dir}")

    # measure time
    with benchmark("main", log):
        log.info("️🏎️ starting ..")
        main()
        log.info("️🏁 done.")
