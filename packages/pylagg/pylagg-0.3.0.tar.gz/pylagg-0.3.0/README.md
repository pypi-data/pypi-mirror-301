# LAGG
A CLI tool for creating images from DNA sequences.

## Installation
Install LAGG using pip with the following command:
```
pip install pylagg
```
## For Developers
Activate virtual environment with ```poetry shell```

```cd pylagg```

To try out commands, type ```lagg <command> <arguments>```

#### Example accession numbers
SRR8782097 will lead to 1 .fastq.gz files 

SRR6670124 will lead to 2 .fastq.gz files

## For Contributors
This project uses [Poetry](https://python-poetry.org) to handle dependencies and build the project.
Installation instructions can be found [here](https://python-poetry.org/docs/#installation).

### Install Dependencies
Use `poetry install` to install all dependencies automatically in a new virtual environment.
If you'd like to install the dependencies directly within the project directory, use the following command:
```
poetry config virtualenvs.in-project true
```

### Running Tests
To run tests, first, activate the virtual environment using `poetry shell`.

Use `pytest` to run all tests.
