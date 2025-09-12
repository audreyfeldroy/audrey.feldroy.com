# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "jupyter",
#     "jupyter-contrib-nbextensions",
#     "nbconvert",
#     "notebook<7",
# ]
# ///
from pathlib import Path
from subprocess import check_call


def main():
    for notebook in Path('nbs').glob('*.ipynb'):
        command = f"jupyter nbconvert --to markdown {notebook} --output-dir articles"
        print(command)
        check_call(command.split(' '))


if __name__=='__main__':
    main()
