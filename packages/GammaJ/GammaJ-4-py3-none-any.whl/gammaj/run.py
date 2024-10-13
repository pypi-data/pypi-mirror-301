import os


def run() -> None:
    import sys
    from importlib import import_module

    parse_gmaj_file = import_module("gammaj.parser").parse_gmaj_file

    try:
        if "γ" in sys.argv[1]:
            print("HINT: '!gamma' is automatically translated to 'γ' when running GammaJ files.\n\n")

        sys.argv[1] = sys.argv[1].replace("!gamma", "γ")

        parse_gmaj_file(sys.argv[1])
    except IndexError:
        print("FATAL: Please provide a file path as an argument.")
    except FileNotFoundError:
        print(f"FATAL: That file could not be found in '{os.getcwd()}'")
    except Exception as err: # NOQA
        print(f"FATAL: UNCAUGHT: An unexpected error occurred on GammaJ's end: {type(err).__name__}\nINFO: {err}")

if __name__ == "__main__":
    run()