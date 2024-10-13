import argparse
import subprocess
import sys

import click


def run_test(exercise):
    test_script = f"test_{exercise}.py"
    subprocess.run([sys.executable, test_script])


@click.command()
@click.argument("exercise")
def checkpadis(exercise):
    """
    Usage: checkpadis [EXERCISE]

    Execute tests for the specified exercise.

    Example:

    - checkpadis 01_hello_world
    """
    parser = argparse.ArgumentParser(description="Library to test exercises")
    parser.add_argument("exercise", type=str, help="Exercise to test")

    args = parser.parse_args()

    run_test(args.exercise)


if __name__ == "__main__":
    checkpadis()
