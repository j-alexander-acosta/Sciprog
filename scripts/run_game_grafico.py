#  Copyright (c) 2026. Programacion Cientifica, DISC, Antofagasta, Chile.
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import convolve2d
from typing import TypeAlias
from benchmarking import benchmark
from logger import configure_logging

# Definición de tipos para claridad
Board: TypeAlias = np.ndarray


def initialize_symmetric_board(size: int) -> Board:
    """Crea un tablero con patrones simétricos para generar visualizaciones mandálicas."""
    board = np.zeros((size, size), dtype=np.uint8)
    # Crear un patrón aleatorio en el cuadrante superior izquierdo
    half = size // 2
    quarter = np.random.choice([0, 1], size=(half, half), p=[0.85, 0.15])

    # Reflejar el patrón en los 4 cuadrantes para asegurar simetría
    board[0:half, 0:half] = quarter
    board[0:half, half:size] = np.flip(quarter, axis=1)
    board[half:size, 0:half] = np.flip(quarter, axis=0)
    board[half:size, half:size] = np.flip(np.flip(quarter, axis=0), axis=1)
    return board


def evolve(board: Board) -> Board:
    """Evolución vectorizada usando convolución (Pipeline de procesamiento)."""
    # Kernel para contar los 8 vecinos
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    # Convolución para contar vecinos de todas las celdas a la vez
    neighbours = convolve2d(board, kernel, mode="same", boundary="wrap")

    # Aplicación de las Reglas de Conway mediante máscaras booleanas
    next_board = np.zeros_like(board)
    # Sobreviven células vivas con 2 o 3 vecinos
    next_board[(board == 1) & ((neighbours == 2) | (neighbours == 3))] = 1
    # Nacen células muertas con exactamente 3 vecinos
    next_board[(board == 0) & (neighbours == 3)] = 1

    return next_board


def main_visualizer():
    """Función principal que gestiona la animación gráfica."""
    size = 200  # Tamaño del universo (escalable gracias a NumPy)
    board = initialize_symmetric_board(size)

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title(
        "Conway's Game of Life - Visualización Científica"
    )

    # 'binary' mapea 0 a blanco y 1 a negro (o viceversa)
    img = ax.imshow(board, cmap="magma", interpolation="nearest")
    ax.axis("off")

    def update(frame):
        nonlocal board
        board = evolve(board)
        img.set_data(board)
        return [img]

    # Crear la animación (intervalo en milisegundos)
    ani = animation.FuncAnimation(
        fig, update, frames=None, interval=50, blit=True, cache_frame_data=False
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    configure_logging(logging.INFO)
    log = logging.getLogger(__name__)

    with benchmark("GameOfLife_Visualizer", log):
        log.info("🏎️ Iniciando visualización de alto rendimiento...")
        main_visualizer()
        log.info("🏁 Simulación finalizada.")
