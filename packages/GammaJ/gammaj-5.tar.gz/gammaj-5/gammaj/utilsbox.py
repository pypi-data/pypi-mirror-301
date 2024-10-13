import os
import subprocess
from typing import Any
from uuid import uuid4

def add_html(path: str, cont: str) -> None:
    with open(path, "a") as file:
        file.write(cont)
def run_html(path: str) -> None:
    if os.path.exists(path):
        with open("vexilconfig.yaml", "w") as file:
            file.write(
"""
logger:
loggingConfig:
  filename: __gammaj__.log
loggingLevel:
loggingFormat:
cleanLogger:
cleanPycache:
cleanLogFile:
"""
            )
            with open(path_t := str(uuid4()), "w") as file2:
                file2.write(
"""
from vexilpy import launch, Server
from random import randint
launch(Server(randint(49152, 65535), "."))
"""
                )
        subprocess.run(["python.exe", path_t], stdout=subprocess.DEVNULL)
        os.remove(path)
        os.remove(path_t)
        os.remove("vexilconfig.yaml")

class Service:
    @staticmethod
    def print(*cont: Any, sep: str | None = None) -> None:
        add_html("index.html", (sep or " ").join([str(c).strip() for c in cont]))
    @staticmethod
    def heading(*cont: Any) -> None:
        Service.print("<h1>", *cont, "</h1>")
    @staticmethod
    def heading2(*cont: Any) -> None:
        Service.print("<h2>", *cont, "</h2>")
    @staticmethod
    def heading3(*cont: Any) -> None:
        Service.print("<h3>", *cont, "</h3>")
    @staticmethod
    def heading4(*cont: Any) -> None:
        Service.print("<h4>", *cont, "</h4>")
    @staticmethod
    def paragraph(*cont: Any) -> None:
        Service.print("<p>", *cont, "</p>")
    @staticmethod
    def weblink(href: str, *cont: Any) -> None:
        Service.print(f"<a href='{href}'>", *cont, "</a>")
    @staticmethod
    def image(src: str, alt: str) -> None:
        Service.print(f"<img src='{src}' alt='{alt}'>")
    @staticmethod
    def list(*items: Any) -> None:
        Service.print("<ul>")
        for item in items:
            Service.print("<li>", item, "</li>")
        Service.print("</ul>")
    @staticmethod
    def table(*rows: Any) -> None:
        Service.print("<table>")
        for row in rows:
            Service.print("<tr>")
            for cell in row:
                Service.print("<td>", cell, "</td>")
            Service.print("</tr>")
        Service.print("</table>")