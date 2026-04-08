from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def main() -> None:
    print("test.py pronto para testes rápidos.")

    try:
        from states.board import Board  # type: ignore

        _ = Board
        print("Import de states.board OK")
    except Exception as exc:
        print(f"Error in import states.board: {exc}")


if __name__ == "__main__":
    main()
