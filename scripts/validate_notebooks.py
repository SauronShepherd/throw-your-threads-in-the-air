from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "notebooks").glob("*.ipynb"))


def main() -> None:
    if len(NOTEBOOKS) != 11:
        raise SystemExit(f"Expected 11 lab notebooks, found {len(NOTEBOOKS)}")
    for path in NOTEBOOKS:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if notebook.get("nbformat") != 4 or not notebook.get("cells"):
            raise SystemExit(f"Invalid notebook structure: {path.name}")
        if any(not cell.get("id") for cell in notebook["cells"]):
            raise SystemExit(f"Notebook cell missing stable id: {path.name}")
        for index, cell in enumerate(notebook["cells"]):
            source = "".join(cell.get("source", []))
            if cell["cell_type"] == "code":
                try:
                    ast.parse(source, filename=f"{path.name}:cell-{index}")
                except SyntaxError as exc:
                    raise SystemExit(f"{path.name}, cell {index}: {exc}") from exc
        print(f"OK {path.name}")
    print(f"Validated {len(NOTEBOOKS)} notebooks and Python code cells.")


if __name__ == "__main__":
    main()
