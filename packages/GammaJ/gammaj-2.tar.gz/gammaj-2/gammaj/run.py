def run() -> None:
    import sys
    from importlib import import_module

    parse_gmaj_file = import_module("gammaj.parser").parse_gmaj_file

    try:
        parse_gmaj_file(sys.argv[1])
    except Exception as err: # NOQA
        print(f"FATAL: An error occurred while parsing GammaJ: {type(err).__name__}\nFETCHED INFO: {err}")

if __name__ == "__main__":
    run()