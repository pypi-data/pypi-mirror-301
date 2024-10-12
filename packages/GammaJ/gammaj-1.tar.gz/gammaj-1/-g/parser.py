from uuid import uuid4


def parse_gmaj(code: str) -> tuple[str, str]:
    uuid = str(uuid4())

    return (
        "from importlib import import_module\n"
        "utilsbox = import_module(\"-g.utilsbox\")\n"
        "del import_module\n"
        + code\
        .replace("<html>", "utilsbox.add_html(\"index.html\", \"\"\"")\
        .replace("</html>", "\"\"\")") \
        .replace("<!DOCTYPE html>", "utilsbox.add_html(\"index.html\", \"<!DOCTYPE html>\")")\
        + "\ndel utilsbox",
        uuid
    )

def parse_gmaj_file(path: str) -> None:
    with open(path) as file:
        code = file.read()
    code, uuid = parse_gmaj(code)
    with open(uuid, "w") as file:
        file.write(code)
    import os
    os.system(f"python.exe \"{uuid}\"")
    from .utilsbox import run_html
    run_html("index.html")
    os.remove(uuid)