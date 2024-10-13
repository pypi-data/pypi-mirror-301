import subprocess
import os
import venv

class Template:
    def __init__(self, name: str):
        self.name = name
        venv_path = ".venv"
        if not os.path.exists(venv_path):
            self.setup_virtual_env()
        self.packages = []

    def setup_virtual_env(self):
        print(f"Setting up virtual environment for {self.name}")
        venv_path = ".venv"
        try:
            # Create virtual environment
            venv.create(venv_path, with_pip=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to set up virtual environment: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    def pip_install(self, *packages):
        self.packages.extend(packages)

    def install_packages(self):
        if self.packages:
            try:
                venv_path = ".venv"
                pip_path = os.path.join(venv_path, 'bin', 'pip')
                subprocess.run([pip_path, "install", *self.packages], check=True)
                print(f"Successfully installed {self.packages} for {self.name}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install packages: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
    
