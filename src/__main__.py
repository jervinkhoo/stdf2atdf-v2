# __main__.py
from .cli import main
# from .utils.logging import setup_logging # Removed, cli.main() handles logging setup

if __name__ == "__main__":
    # setup_logging() # Removed, cli.main() handles logging setup
    main()