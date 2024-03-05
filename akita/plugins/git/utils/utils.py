import subprocess


def get_staged_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            check=True,
            text=True,
            capture_output=True,
        )
        staged_files = result.stdout.splitlines()
        return staged_files
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving staged files: {e}")
        return []


def get_staged_diff():
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            check=True,
            text=True,
            capture_output=True,
        )
        staged_diff = result.stdout
        return staged_diff
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving staged diff: {e}")
        return ""


def get_diff():
    try:
        result = subprocess.run(
            ["git", "diff"],
            check=True,
            text=True,
            capture_output=True,
        )
        staged_diff = result.stdout
        return staged_diff
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving staged diff: {e}")
        return ""
