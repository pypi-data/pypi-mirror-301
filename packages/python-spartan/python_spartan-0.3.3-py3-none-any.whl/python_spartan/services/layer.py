import json
import os
import shutil
import subprocess
import sys
import zipfile


class LayerService:
    def __init__(
        self,
        requirements_file="requirements.txt",
        venv_lib_path=".venv/lib",
        layer_name="spartan_lambda_layer",
        compatible_runtimes=None,
        description="",
        verbose=False,
    ):
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.requirements_file = requirements_file
        path = f"./{layer_name}/lib/{python_version}/site-packages"
        self.target_directory = path
        self.venv_lib_path = venv_lib_path
        self.layer_name = layer_name
        self.description = description
        self.compatible_runtimes = (
            compatible_runtimes if compatible_runtimes else ["python3.11"]
        )
        self.verbose = verbose

    def check_virtual_environment(self):
        if os.getenv("VIRTUAL_ENV") is None:
            print(
                "Error: You are not in a virtual environment. Please activate a virtual environment and try again."
            )
            sys.exit(1)
        if self.verbose:
            print("Virtual environment detected.")

    def install_requirements(self):
        pip_command = [
            "pip",
            "install",
            "-r",
            self.requirements_file,
            "--platform",
            "manylinux2014_x86_64",
            "--only-binary=:all:",
            "--target",
            self.target_directory,
        ]

        try:
            result = subprocess.run(
                pip_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if self.verbose:
                print(result.stdout.decode())
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print("An error occurred while installing dependencies:")
            if self.verbose:
                print(e.stderr.decode())

    def create_python_directory(self, python_directory="python"):
        if not os.path.exists(python_directory):
            os.makedirs(python_directory)
            if self.verbose:
                print(f"Created directory: {python_directory}")

        if os.path.exists(self.venv_lib_path):
            shutil.copytree(
                self.venv_lib_path,
                os.path.join(python_directory, "lib"),
                dirs_exist_ok=True,
            )
            print(f"Copied python packages")
        else:
            print(f"Virtual environment lib folder not found at {self.venv_lib_path}")

    def zip_directory(self, directory, zip_filename):
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.join(directory, ".."))
                    zipf.write(file_path, arcname)
        print(f"Compressed python packages into {zip_filename}")

    def clean_up_directories(self, directories):
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                if self.verbose:
                    print(f"Removed directory: {directory}")

    def build_layer(self):
        self.check_virtual_environment()
        self.install_requirements()
        self.create_python_directory()
        zip_filename = f"{self.layer_name}.zip"
        self.zip_directory("python", zip_filename)
        self.clean_up_directories([self.layer_name, "python"])
        return zip_filename
