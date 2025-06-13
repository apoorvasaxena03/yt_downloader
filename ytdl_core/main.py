import sys
from .cli import run_cli
from .gui import launch_gui

def main():
    if len(sys.argv) == 1:
        launch_gui()
    else:
        run_cli()

if __name__ == "__main__":
    main()