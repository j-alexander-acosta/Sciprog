#  Copyright (c) $today.year.Programación Científica DISC Antofagasta, Chile
import logging
import numpy as np
from prettytable import PrettyTable
from tqdm import tqdm
from scipy.signal import convolve2d  # Para contar vecinos de forma ultra rápida
from benchmarking import benchmark
from logger import configure_logging
from typing import TypeAlias

# Definimos el tipo como un arreglo de NumPy
Board: TypeAlias = np.ndarray

log = logging.getLogger(__name__)


def show_board(board: Board) -> None:
    table = PrettyTable()
    ncols = board.shape[1]
    table.field_names = ["r\\c"] + [str(c) for c in range(ncols)]
    table.hrules = True

    for r, row in enumerate(board):
        table.add_row([str(r)] + ["█" if cell == 1 else "·" for cell in row])
    log.debug(f"\n{table}")


def expand(board: Board) -> Board:
    """Añade un marco de ceros usando np.pad."""
    return np.pad(board, pad_width=1, mode="constant", constant_values=0)


def compact(board: Board) -> Board:
    """Elimina filas y columnas de ceros en los bordes usando slicing."""
    # Encontrar las filas y columnas que no son todo ceros
    rows = np.any(board != 0, axis=1)
    cols = np.any(board != 0, axis=0)

    # Si el tablero está vacío, devolvemos una matriz mínima
    if not np.any(rows) or not np.any(cols):
        return np.zeros((3, 3), dtype=int)

    # Aplicar el recorte
    return board[np.ix_(rows, cols)]


def evolve(board: Board) -> Board:
    """Evolución vectorizada usando convolución y reglas booleanas."""
    board = expand(board)

    # Kernel para contar los 8 vecinos (el centro es 0 para no contarse a sí mismo)
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    # Convolve2d cuenta los vecinos de todas las celdas simultáneamente
    neighbours = convolve2d(board, kernel, mode="same")

    # Aplicamos las reglas de Conway mediante máscaras booleanas
    next_board = np.zeros_like(board)

    # Regla: Célula viva sobrevive si tiene 2 o 3 vecinos
    next_board[(board == 1) & ((neighbours == 2) | (neighbours == 3))] = 1
    # Regla: Célula muerta nace si tiene exactamente 3 vecinos
    next_board[(board == 0) & (neighbours == 3)] = 1

    return compact(next_board)


def main() -> None:
    max_iterations = 500
    # Inicializamos con NumPy (dtype=int para ahorrar memoria)
    board = np.array(
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 1, 0],
        ],
        dtype=int,
    )

    show_board(board)

    for _ in tqdm(range(max_iterations)):
        board = evolve(board)

    show_board(board)


if __name__ == "__main__":
    configure_logging(logging.DEBUG)
    log = logging.getLogger(__name__)

    with benchmark("main", log):
        log.info("🏎️ starting (NumPy optimized) ..")
        main()
        log.info("🏁 done.")
