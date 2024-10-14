from pathlib import Path

current_path = Path(__file__).resolve()
print(current_path.parent.parent)