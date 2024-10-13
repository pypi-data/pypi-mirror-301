import os
import re
import subprocess


class TestService:
    def __init__(
        self,
        name: str = None,
        integration=False,
        coverage=False,
        report=None,
        output_path=None,
    ):
        self.name = name
        self.coverage = coverage
        self.report = report
        self.integration = integration
        self.home_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.current_directory = os.getcwd()

        # Decide whether to place the test in tests/unit or tests/feature, or use the custom output path
        if output_path:
            self.destination_folder = output_path
        else:
            self.destination_folder = (
                "tests/feature" if self.integration else "tests/unit"
            )

        if self.name:
            self.file_name = re.sub(r"\d", "", f"test_{self.name}.py").lower()
            self.file_path = os.path.join(self.destination_folder, self.file_name)

        # Define the folder where the stubs are located
        self.stub_folder = os.path.join(self.home_directory, "stubs", "test")
        self.source_stub = self.determine_source_stub()

    def determine_source_stub(self):
        """
        Determine which stub file to use as a template for the test file.
        In this case, it defaults to the 'default.stub' file.
        """
        return os.path.join(self.stub_folder, "default.stub")

    def create_test_file(self):
        """
        Create a new test file using the template from the stub folder.
        """
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)

        if os.path.exists(self.file_path):
            print(f"Test file {self.file_path} already exists!")
        else:
            try:
                # Read the stub template
                with open(self.source_stub, "r") as template_file:
                    template_content = template_file.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"Template file {self.source_stub} not found!")

            # Replace placeholders in the template
            test_content = template_content.replace("{{test_name}}", self.name).replace(
                "{{TestClassName}}", self.name.capitalize()
            )

            # Write the new test file with the updated content
            with open(self.file_path, "w") as f:
                f.write(test_content)

            print(f"Test file {self.file_path} created.")

    def run_tests(self):
        """
        Run the tests in the entire tests folder (tests/unit, tests/feature, etc.).
        Optionally run with coverage and reports.
        """
        test_folder = "tests"

        if not os.path.exists(test_folder):
            print(
                f"Test directory '{test_folder}' does not exist. Please create tests first."
            )
            return

        command = ["pytest", test_folder]

        if self.coverage:
            command.append("--cov")

        if self.report:
            command.append(f"--cov-report={self.report}")

        try:
            result = subprocess.run(command, check=True)
            print(f"Test run completed")
        except subprocess.CalledProcessError as e:
            print(f"Test run failed: {e}")
