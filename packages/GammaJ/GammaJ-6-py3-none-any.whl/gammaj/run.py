import os


def run() -> None:
    import sys
    from importlib import import_module

    parse_gmaj_file = import_module("gammaj.parser").parse_gmaj_file

    try:
        sys.argv[1]
    except IndexError:
        print("FATAL: Please provide a file path as an argument.")
    try:
        parse_gmaj_file(sys.argv[1])
    except FileNotFoundError:
        print(f"FATAL: That file could not be found in '{os.getcwd()}'")
    except Exception as err: # NOQA
        print(f"FATAL: UNCAUGHT: An unexpected error occurred on GammaJ's end: {type(err).__name__}\nINFO: {err}")
        if "--verbose" in sys.argv:
            raise err

if __name__ == "__main__":
    run()