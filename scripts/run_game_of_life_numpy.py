#  Copyright (c) 2026. Programacion Cientifica, DISC, Antofagasta, Chile.
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from prettytable import PrettyTable

import numpy as np

from benchmarking import benchmark  # ty:ignore[unresolved-import]
from logger import configure_logging  # ty:ignore[unresolved-import]


@dataclass
class GameOfLife:
    """The Game of Life class"""

    # the board
    board: np.ndarray

    # the current generation
    generation: int = 0

    # the max number of generations
    max_generations: int = 10000

    # the representation of a dead cell
    dead_cell: str = "·"

    # the representation of a live cell
    alive_cell: str = "█"

    # constants
    ALIVE: ClassVar[int] = 1
    DEAD: ClassVar[int] = 0

    def __post_init__(self) -> None:
        """Post-initialization check for the Game of Life class"""

        # The board needs to be a ndarray
        if not isinstance(self.board, np.ndarray):
            raise TypeError("The board must be a numpy array")

        # The board needs to be a unit8
        if self.board.dtype != np.uint8:
            self.board = self.board.astype(np.uint8)

        # The board needs to be a 2 dimensional array
        if self.board.ndim != 2:
            raise TypeError("The board must be a 2-dimensional array")

        # All the cell in the board needs to be ALIVE/DEAD
        if not np.all(np.isin(self.board, [self.DEAD, self.ALIVE])):
            raise TypeError("The board must contain only zeros or ones")

        # The max generations needs to be positive
        if self.max_generations <= 0:
            raise TypeError("The max_generations must be a positive integer")

    @classmethod
    def from_list(cls, initial_state: list[list[int]]) -> "GameOfLife":
        """Create a GameOfLife class from a list of states"""

        if not initial_state:
            raise TypeError("The initial_state must be a list")

        if not all(isinstance(state, list) for state in initial_state):
            raise ValueError("The initial_state must be a list")

        return cls(board=np.array(initial_state))

    # def __str__(self) -> str:
    #     # TODO: Use the PrettyTable to show the board in ascii.
    #     table = PrettyTable()
    #     table.header = False
    #     table.border = True
    #
    #     for row in self.board:
    #         table.add_row(
    #             [
    #                 self.alive_cell if cell == self.ALIVE else self.dead_cell
    #                 for cell in row
    #             ]
    #         )
    #
    #     return f"Generation: {self.generation}\n{table}"

    def __str__(self) -> str:
        """Utiliza PrettyTable para mostrar el tablero en formato ASCII."""
        from prettytable import PrettyTable

        table = PrettyTable()

        # Obtener dimensiones del tablero de NumPy
        n_rows, n_cols = self.board.shape

        # Configurar cabecera: r\c seguido de los índices de columna
        table.field_names = ["r\\c"] + [str(c) for c in range(n_cols)]

        # Activar las reglas horizontales para mejor legibilidad
        table.hrules = True

        # Poblar la tabla con los caracteres definidos en la clase (· y █)
        for r in range(n_rows):
            # Traducir los valores 1/0 a los caracteres visuales definidos en el dataclass
            row_visual = [
                self.alive_cell if cell == self.ALIVE else self.dead_cell
                for cell in self.board[r]
            ]
            table.add_row([str(r)] + row_visual)

        return f"\nGeneración: {self.generation}\n{table.get_string()}"

def main():
    # init -> board 3x3
    board = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 1, 0],
    ]

    # list[list[int]] -> GameOfLife
    gof = GameOfLife.from_list(board)

    log.debug(f"gof: {gof}")


# call the main function
if __name__ == '__main__':
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