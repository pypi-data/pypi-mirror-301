import typer
import subprocess
import sys
import os
import importlib.util
from .app import App

app = typer.Typer()

@app.command()
def deploy(file: str):
    """
    Deploy a Python script to Jarvislabs.
    """
    print("deployed")

@app.command()
def run(file: str):
    """
    Run a Python script using the jarvislabs environment.
    """
    try:
        # Load the user's script as a module
        spec = importlib.util.spec_from_file_location("user_script", file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Find the App instance in the user's script
        app_instance = next((obj for obj in user_module.__dict__.values() if isinstance(obj, App)), None)

        if app_instance is None:
            typer.echo("Error: No jarvislabs App instance found in the script.")
            raise typer.Exit(code=1)

        # Install packages
        app_instance.template.install_packages()

        # Create and change to the 'models' directory
        models_dir = os.path.join(os.getcwd(), "models")
        os.makedirs(models_dir, exist_ok=True)
        os.chdir(models_dir)

        # Run build_fn in the 'models' directory
        app_instance.build_fn()

        # Change back to the original directory
        os.chdir(os.path.dirname(os.path.abspath(file)))

        # Import Server class
        from jarvislabs import Server

        # Create and run the server
        server = Server(app_instance)
        server.run()

    except ImportError as e:
        typer.echo(f"Error importing jarvislabs or user script: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An error occurred while running the script: {e}")
        raise typer.Exit(code=1)
    
@app.callback()
def callback():
    """
    Jarvislabs CLI for running Python scripts and managing the environment.
    """

if __name__ == "__main__":
    app()