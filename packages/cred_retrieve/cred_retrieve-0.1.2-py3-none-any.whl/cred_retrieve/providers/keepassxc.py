import os
import winreg
import subprocess
from reg_query import WIN64READ, traverse

from ..provider import CredentialProvider

def match_displayname(app_name: str):
    """Return a function to match registry entries by display name."""
    def match(subkey):
        display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
        if app_name.lower() in display_name.lower():
            install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
            if install_location:
                return True, install_location
        return False, None
    return match

registry_paths = (
    r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
)

def get_keepassxc_install_path() -> str:
    """Retrieve the installation path for KeePassXC."""
    match = match_displayname('keepassxc')
    rv = traverse(registry_paths[0], match, WIN64READ)
    if not rv:
        rv = traverse(registry_paths[1], match, WIN64READ)
    return rv

def get_keepassxc_path() -> str:
    """Get the path to the KeePassXC CLI executable."""
    base = get_keepassxc_install_path()
    if not base:
        return None
    return os.path.join(base, 'keepassxc-cli.exe')

#def get_id_pw(database_path: str, password: str, entry_title: str) -> list:
#    """Retrieve username and password from KeePassXC."""
#    try:
#        # Construct the command to retrieve the password
#        command = [
#            get_keepassxc_path(), 'show', '-qsa', 'username',
#            '-sa', 'password',
#            database_path,
#            entry_title
#        ]
#
#        # Run the command securely, ensuring sensitive data is handled properly
#        result = subprocess.run(command, input=password, text=True, capture_output=True, check=True)
#        
#        # Extract and return the password
#        return result.stdout.strip().split('\n')
#
#    except subprocess.CalledProcessError as e:
#        print(f"An error occurred while retrieving credentials: {e}")
#        return None
#    except FileNotFoundError:
#        print("KeePassXC CLI not found. Ensure it is installed.")
#        return None

def get_id_pw(database_path: str, password: str, entry_title: str) -> list:
    """Retrieve username and password from KeePassXC."""
    try:
        # Construct the command to retrieve the password
        command = [
            get_keepassxc_path(), 'show', '-qsa', 'username',
            '-sa', 'password',
            database_path,
            entry_title
        ]

        # Start the subprocess
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # Send the password and capture the output
        stdout, stderr = process.communicate(input=password)

        # Check if the process completed successfully
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command, output=stdout, stderr=stderr)

        # Extract and return the username and password
        return stdout.strip().split('\n')

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while retrieving credentials: {e.stderr}")
        return None
    except FileNotFoundError:
        print("KeePassXC CLI not found. Ensure it is installed.")
        return None



class Provider(CredentialProvider):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_id_pw(self, db_pw: str, entry: str) -> list:
        """Get ID and password using the provided database path and entry."""
        #return get_id_pw(self.db_path, self.db_pw, self.entry)
        return get_id_pw(self.db_path, db_pw, entry)
