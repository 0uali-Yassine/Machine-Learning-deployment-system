#!/usr/bin/env python3
"""
Build script for creating standalone Python executable using PyInstaller.
"""

import subprocess
import sys
from pathlib import Path
import time

# Get the project root directory
project_root = Path(__file__).parent

# Define paths
main_script_path = project_root / "main.py"
model_file_path = project_root / "model" / "core_model.pkl"

def build_executable():
    """Build the standalone executable."""

    # Verify files exist
    if not main_script_path.exists():
        print(f"Error: {main_script_path} not found!")
        sys.exit(1)

    if not model_file_path.exists():
        print(f"Error: {model_file_path} not found!")
        sys.exit(1)

    # Example command:
    # uv run pyinstaller --onefile --name predict --add-data "src/model/core_model.pkl:." src/main.py
    # Build PyInstaller command - much simpler with --collect-all
    cmd = [
        "uv", "run", "pyinstaller",
        "--onefile",
        "--distpath", "../dist",
        "--workpath", "../build",
        "--log-level", "WARN",
        "--name", "exe",
        "--add-data", f"model/core_model.pkl:.",  # or model/core_model.joblib:.,
        "--collect-all", "sklearn",  # Automatically collects all sklearn submodules
        str(main_script_path)
    ]

    print("Building executable...")
    print("\033[94m", end="")
    print(f" Command: {' '.join(cmd)}", end="")
    print("\033[0m")
    print()

    # Run the command
    start_time = time.time()
    result = subprocess.run(cmd, cwd=project_root)
    build_time = time.time() - start_time

    if result.returncode == 0:
        print(
            f"\n✅ Build completed in {build_time:.2f} seconds, executable is in ../dist/predict"
        )
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

    cleanup_build_shit()


def cleanup_build_shit():
    """Cleanup build build and spec files."""
    try:
        # Remove the build directory
        build_dir = (project_root.parent / "build").resolve()
        spec_file = (project_root / "predict.spec").resolve()
        if build_dir.exists() and spec_file.exists():
            cmd = ["rm", "-rf", str(build_dir), str(spec_file)]
            # Run the command
            result = subprocess.run(cmd, cwd=project_root.parent)

            if result.returncode == 0:
                print("\n✅ Cleanup complete!")
            else:
                print("\n❌ Cleanup failed!")
                sys.exit(1)
        else:
            print(f"\n❌ Cleanup failed: {build_dir} does not exist")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Cleanup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
