import requests
import importlib

class UpdateChecker:
    def check_for_updates(self):
        try:
            current_version = importlib.import_module("auth_key_manager.__version__").__version__
            module_name = importlib.import_module("auth_key_manager.__version__").__module_name__
            response = requests.get(f"https://pypi.org/pypi/{module_name}/json")
            releases = response.json()["releases"]
            
            latest_version = sorted(releases.keys(), key=lambda s: list(map(int, s.split("."))), reverse=True)[0]

            if current_version != latest_version:
                print(f"Update available: {latest_version}. You are currently using {current_version}.")
            else:
                pass
        except Exception as e:
            print(f"Error checking for updates: {str(e)}")
