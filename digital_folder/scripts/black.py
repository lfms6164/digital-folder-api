import subprocess
import os


def run_black():
    # Path to the digital_folder directory
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"Formatting Python files in: {target_dir}")

    # Run Black with explicit encoding handling
    result = subprocess.run(
        ["black", target_dir], capture_output=True, text=True, encoding="utf-8"
    )

    # Print Black's output and handle potential errors
    print(result.stdout)
    if result.stderr:
        print(f"Errors:\n{result.stderr}")


if __name__ == "__main__":
    run_black()
