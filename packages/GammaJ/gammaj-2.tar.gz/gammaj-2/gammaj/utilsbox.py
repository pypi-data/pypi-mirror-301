import os
import subprocess
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
  filename: throwaway.log
loggingLevel:
loggingFormat:
cleanLogger:
cleanPycache:
cleanLogFile: true
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