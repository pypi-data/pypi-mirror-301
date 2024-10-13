import sys
from uuid import uuid4


def parse_gmaj(code: str) -> tuple[str, str]:
    uuid = str(uuid4())
    code = \
        "from gammaj import utilsbox\n"\
        + code\
        .replace("export <void>", "utilsbox.add_html(\"index.html\", \"\"\"")\
        .replace("</void>", "\"\"\")") \
        .replace("export ", "utilsbox.Service.")\
        + "\ndel utilsbox"

    lns: list[str] = code.split("\n")
    indent: int = 0
    new_code: list[list[str]] = []
    in_string: bool = False

    for ln_num, ln in enumerate(lns):
        ln = (" " * indent) + ln.lstrip(" ")
        new_code.append([])
        for index, char in enumerate(ln):
            if char in "\"'":
                in_string = not in_string
                new_code[-1].append(char)
            elif char == "{" and not in_string:
                if ln[index - 1] != "$":
                    indent += 4
                    new_code[-1].append(":")
                    lns.insert(ln_num + 1, ln[index:].removeprefix("{"))
                    break
            elif char == "}" and not in_string:
                if len(ln) == index:
                    if ln[index + 1] == "$":
                        continue

                indent -= 4
            else:
                new_code[-1].append(char)

    return "\n".join(["".join(c) for c in new_code]), uuid

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
    if "--no-delete" not in sys.argv:
        os.remove(uuid)