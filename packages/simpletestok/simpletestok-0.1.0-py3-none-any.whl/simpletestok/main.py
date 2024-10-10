import subprocess

def get_current_user():
    """Execute the 'whoami' command and return the current user."""
    result = subprocess.run(["whoami"], capture_output=True, text=True)
    return result.stdout.strip()
