from pathlib import Path
import os


def transform_name(name: str) -> str:
    # Remove all leading underscores
    name = name.lstrip("_")
    # Replace all remaining underscores with spaces
    return name.replace("_", " ")


def rename_recursive(root="."):
    # Rename deepest paths first so directories are renamed safely
    paths = sorted(
        Path(root).rglob("*"),
        key=lambda p: len(p.parts),
        reverse=True,
    )

    for path in paths:
        new_name = transform_name(path.name)

        if new_name == path.name:
            continue

        new_path = path.with_name(new_name)

        try:
            os.rename(path, new_path)
            print(f"Renamed: {path} -> {new_path}")
        except FileExistsError:
            print(f"Skipped (already exists): {new_path}")
        except Exception as e:
            print(f"Failed: {path} ({e})")


if __name__ == "__main__":
    rename_recursive(".")
