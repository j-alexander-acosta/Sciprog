import logging
import copy # Importante para la copia profunda
from prettytable import PrettyTable
from benchmarking import benchmark
from logger import configure_logging

log = logging.getLogger(__name__)

def show_board(board):
    table = PrettyTable()
    table.header = False
    table.hrules = True
    for row in board:
        table.add_row(["⬛" if cell == 1 else "⬜" for cell in row])
    # Imprimir la tabla completa después del bucle
    log.debug(f"\n{table}")

def count_neighbours(board, row, column):
    sum = 0
    for r in range(row - 1, row + 2):
        for c in range(column - 1, column + 2):
            if r == row and c == column:
                continue
            if 0 <= r < len(board) and 0 <= c < len(board[0]):
                if board[r][c] == 1:
                    sum += 1
    return sum

def evolve(board):
    # Crear una copia real para no modificar el original mientras contamos
    next_board = copy.deepcopy(board)

    for row in range(len(board)):
        for column in range(len(board[row])):
            # Contamos sobre el board original
            neighbours = count_neighbours(board, row, column)

            if board[row][column] == 1:
                # Supervivencia o Muerte
                if neighbours < 2 or neighbours > 3:
                    next_board[row][column] = 0
            else:
                # Nacimiento
                if neighbours == 3:
                    next_board[row][column] = 1

    return next_board # Retornar después de procesar todas las filas

def main():
    max_iterations = 5 # Aumentado para ver evolución
    board = [
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 1],
    ]

    show_board(board)

    for i in range(max_iterations):
        log.debug(f"-- iteration: {i + 1} {'-' * 20}")
        board = evolve(board)
        show_board(board)

if __name__ == "__main__":
    configure_logging(logging.DEBUG)
    with benchmark("main", log):
        log.info("🏎️ starting ..")
        main()
        log.info("🏁 done.")