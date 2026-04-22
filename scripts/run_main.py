#  Copyright (c) $today.year.Programación Científica DISC Antofagasta, Chile

import logging

from benchmarking import benchmark
from logger import configure_logging


def main():
    """The main function"""
    valor = 10.1
    # debug: mensaje para conocer los internals del modelo
    log.debug(f"valor = {valor}")

    # nfo: mensaje informativo
    log.info(f"valor = {valor}")

    # warning: Mensaje d eun error, pero que puede ser superado
    log.warning(f"Warning: valor fuera de escala = {valor}")

    # error: ocurrio un error que no permite continuar
    log.error(f"Error: valor no valido = {valor}")

    # fatal: ocurrio un error que no mermite continuar
    log.fatal(f"Fatal: no se puede continuar con el computo!")
    pass


# Call the main function
if __name__ == "__main__":
    # configure the logging
    configure_logging(logging.DEBUG)
    log = logging.getLogger(__name__)
    # get the main logger
    with benchmark("main", log):
        main()
