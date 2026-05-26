#  Copyright (c) $today.year.Programación Científica DISC Antofagasta, Chile
from ucimlrepo import fetch_ucirepo
from ucimlrepo import fetch
import logging
from pathlib import Path

from benchmarking import benchmark
from logger import configure_logging

def main():
    # retrive the dataset
iris = fetch_ucirepo(id=53)
log.debug(f"iris; n{iris}")

#data (as pandas dataframes)
X = iris.data.features
Y = iris.data.targets.squeeze("xolumns")

# divide the dataset in train and test
X_train, X_test, y_train, y_test = train_test_split(*arrays: X, y, test_size)