import subprocess
import sys

def install(package):
    """method to install packages using pip

    Args:
        package (str): Name of the package
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    # Example usage: install a specific package
    install("gspread")
    install("oauth2client")
    install("google-api-python-client")
    install("google-auth-httplib2")
    install("google-auth-oauthlib")
    install("google-auth")

