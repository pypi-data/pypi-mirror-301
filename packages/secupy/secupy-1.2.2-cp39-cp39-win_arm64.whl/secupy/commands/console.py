import code
import pathlib


def main(filename_path: str):
    filename = pathlib.Path(filename_path)
    if not filename.exists():
        raise RuntimeError("File not found")

    source = filename.read_text()
    ic = code.InteractiveConsole(locals={"__name__": "__main__"})
    ic.runsource(source, filename=filename_path, symbol="exec")
