import os
import shutil
import subprocess
import sys
from typing import Optional

import typer
from alembic.config import Config

from python_spartan.services.application import ApplicationService
from python_spartan.services.deployment import DeploymentService
from python_spartan.services.handler import HandlerService
from python_spartan.services.infrastructure import InfrastructureService
from python_spartan.services.inspire import InspireService
from python_spartan.services.layer import LayerService
from python_spartan.services.migrate import MigrateService
from python_spartan.services.model import ModelService

# from python_spartan.services.parser import ParserService
# from python_spartan.services.plotter import PlotterService
from python_spartan.services.request import RequestService
from python_spartan.services.response import ResponseService
from python_spartan.services.route import RouteService
from python_spartan.services.service import ServiceService
from python_spartan.services.test import TestService

alembic_cfg = Config("alembic.ini")

app = typer.Typer(no_args_is_help=True)


model_app = typer.Typer()
app.add_typer(
    model_app, name="model", help="Manages the creation and deletion of model classes."
)

# parser_app = typer.Typer()
# app.add_typer(
#     parser_app,
#     name="parser",
#     help="Manages the creation and deletion of parser classes.",
# )


# plotter_app = typer.Typer()
# app.add_typer(
#     plotter_app,
#     name="plotter",
#     help="Manages the creation and deletion of plotter classes.",
# )


handler_app = typer.Typer()
app.add_typer(
    handler_app,
    name="handler",
    help="Manages the creation and deletion of lambda files in the application.",
)

migrate_app = typer.Typer()
app.add_typer(
    migrate_app,
    name="migrate",
    help="Manages database changes, like updates, rollbacks, and making new tables.",
)

request_app = typer.Typer()
app.add_typer(
    request_app,
    name="request",
    help=" Manages the creation and deletion of request classes.",
)

service_app = typer.Typer()
app.add_typer(
    service_app,
    name="service",
    help=" Manages the creation and deletion of service classes.",
)

route_app = typer.Typer()
app.add_typer(
    route_app,
    name="route",
    help=" Manages the creation and deletion of route classes.",
)

response_app = typer.Typer()
app.add_typer(
    response_app,
    name="response",
    help=" Manages the creation and deletion of response classes.",
)

db_app = typer.Typer()
app.add_typer(db_app, name="db", help="Prepare your database tables.")

deploy_app = typer.Typer()
app.add_typer(
    deploy_app, name="deploy", help="Optimize your serverless project for deployment."
)

infra_app = typer.Typer()
app.add_typer(
    infra_app, name="infra", help="Setup your serverless infrastructure as a code."
)

layer_app = typer.Typer()
app.add_typer(
    layer_app, name="layer", help="Compress local packages into single zip file."
)

test_app = typer.Typer()
app.add_typer(test_app, name="test", help="Run and create tests.")


def run_poetry_command(command):
    try:
        result = subprocess.run(
            ["poetry", command], capture_output=True, text=True, check=True
        )

        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Command output:", e.output)


def is_valid_folder_name(name):
    """
    Check if a given string is a valid folder name.
    """

    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-")

    return all(char in valid_chars for char in name)


@model_app.command("create", help="Create a new model class.")
def model_create(name: str):
    try:
        service = ModelService(name)
        service.create_model_file()
    except Exception as e:
        print(f"Error creating model: {e}")


# @parser_app.command("create", help="Create a new parser class.")
# def parser_create(name: str):
#     try:
#         service = ParserService(name)
#         service.create_parser_file()
#     except Exception as e:
#         print(f"Error creating parser: {e}")


# @plotter_app.command("create", help="Create a new plotter class.")
# def plotter_create(name: str):
#     try:
#         service = PlotterService(name)
#         service.create_plotter_file()
#     except Exception as e:
#         print(f"Error creating plotter: {e}")


@model_app.command("delete", help="Delete an existing model class.")
def model_delete(name: str):
    try:
        service = ModelService(name)
        service.delete_model_file()
    except Exception as e:
        print(f"Error deleting model: {e}")


@service_app.command("create", help="Create a service class.")
def service_create(name: str):
    try:
        service = ServiceService(name)
        service.create_service_file()
    except Exception as e:
        print(f"Error creating service: {e}")


@route_app.command("create", help="Create a route class.")
def route_create(name: str):
    try:
        route = RouteService(name)
        route.create_route_file()
    except Exception as e:
        print(f"Error creating route: {e}")


@service_app.command("delete", help="Delete an existing service class.")
def service_delete(name: str):
    try:
        service = ServiceService(name)
        service.delete_service_file()
    except Exception as e:
        print(f"Error deleting service: {e}")


@route_app.command("delete", help="Delete an existing route class.")
def route_delete(name: str):
    try:
        route = RouteService(name)
        route.delete_route_file()
    except Exception as e:
        print(f"Error deleting route: {e}")


@handler_app.command(
    "create",
    help="Create a new handler file with optional subscribe and publish options.",
)
def handler_create(
    name: str,
    subscribe: str = typer.Option(None, "--subscribe", "-s", help="Subscribe option."),
    publish: str = typer.Option(None, "--publish", "-p", help="Publish option."),
):
    try:
        handler_service = HandlerService(name, subscribe=subscribe, publish=publish)
        handler_service.create_handler_file()
    except Exception as e:
        print(f"Error creating handler: {e}")


@handler_app.command("delete", help="Delete an existing handler file.")
def handler_delete(name: str):
    try:
        handler_service = HandlerService(name)
        handler_service.delete_handler_file()
    except Exception as e:
        print(f"Error deleting handler: {e}")


@migrate_app.command(
    "upgrade", help="Upgrade the database schema to the latest version."
)
def migrate_upgrade():
    try:
        migrate_service = MigrateService(alembic_cfg)
        migrate_service.migrate_upgrade()
    except Exception as e:
        print(f"Error upgrading database: {e}")


@migrate_app.command(
    "create", help="Create a new database migration with an optional message."
)
def migrate_create(
    message: str = typer.Option("", "--comment", "-c", help="Message option."),
):
    try:
        migrate_service = MigrateService(alembic_cfg)
        migrate_service.migrate_create(message=message)
    except Exception as e:
        print(f"Error creating database migration: {e}")


@migrate_app.command(
    "downgrade", help="Downgrade the database schema to a previous version."
)
def migrate_downgrade():
    try:
        migrate_service = MigrateService(alembic_cfg)
        migrate_service.migrate_downgrade()
    except Exception as e:
        print(f"Error downgrading database: {e}")


@migrate_app.command("refresh", help="Refresh the database migrations.")
def migrate_refresh():
    try:
        migrate_service = MigrateService(alembic_cfg)
        migrate_service.migrate_refresh()
    except Exception as e:
        print(f"Error refreshing database migrations: {e}")


@migrate_app.command(
    "init", help="Initialize database migration with a specified database type."
)
def migrate_init(
    database: str = typer.Option(
        None, "--database", "-d", help="The database type (sqlite, mysql, or psql).."
    )
):
    try:
        migrate_service = MigrateService(alembic_cfg)

        # Validate the database type
        if database not in ["sqlite", "mysql", "psql"]:
            typer.echo(
                "Invalid or no database type specified. Please choose from 'sqlite', 'mysql', or 'psql'."
            )
            raise typer.Exit()

        # Proceed with migration initialization
        migrate_service.migrate_initialize(database)
        typer.echo(f"Migration initialized for database type: {database}")
    except Exception as e:
        print(f"Error initializing database migration: {e}")


@db_app.command("seed", help="Seed the database with initial data.")
def db_seed():
    try:
        print("Seeding the database")
        if sys.platform == "darwin":
            subprocess.run(["python3", "-m", "database.seeders.database_seeder"])
        else:
            subprocess.run(["python", "-m", "database.seeders.database_seeder"])
        print("Done")
    except Exception as e:
        print(f"Error seeding the database: {e}")


@infra_app.command("init", help="Copy a YAML file for infrastructure as code.")
@deploy_app.command("init", help="Copy a YAML file for infrastructure as code.")
def deploy_config(
    source: Optional[str] = typer.Option(
        None, help="Source file path (absolute or relative)"
    )
):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if source is None:
        destination = os.path.join(os.getcwd(), "serverless.yml")

        if os.path.exists(destination):
            typer.echo(
                "'serverless.yml' already exists in the current directory. Aborting."
            )
            raise typer.Abort()

        try:
            stub_file = os.path.join(
                base_dir, "stubs", "infrastructure", "serverless.stub"
            )

            shutil.copy(stub_file, destination)
            typer.echo(
                "File generated to the current working directory as 'serverless.yml'."
            )
        except Exception as e:
            typer.echo(f"Error copying file: {e}")
        return

    try:
        deployment_service = DeploymentService()
        deployment_service.config(source)
    except Exception as e:
        typer.echo(f"Error configuring deployment: {e}")


@app.command("serve", help="Serve the application on a specified port.")
def serve(port: int = typer.Option(8888, "--port", "-p", help="Set port number.")):
    poetry_command = f"poetry run uvicorn public.main:app --reload --port {port}"

    current_dir = os.getcwd()
    main_file_path = os.path.join(current_dir, "public", "main.py")

    if not os.path.exists(main_file_path):
        typer.echo("Spartan is in headless mode. This is not an API project.")
        raise typer.Exit()

    try:
        subprocess.run(poetry_command, shell=True, check=True)
    except Exception as e:
        typer.echo(f"Error running the application. {e}")


# Add the 'create' subcommand
@test_app.command("create")
def create_test(
    test_name: str,
    integration: bool = typer.Option(
        False, "--integration", "-i", help="Create an integration test."
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="Specify the output directory for the test file."
    ),
):
    """
    Create a new test file with the specified name. Use --integration to create an integration test inside tests/feature.
    Use --output to specify a custom output directory for the test file.
    """
    try:
        # Create a new test file using TestService, pass integration flag and output path
        test_service = TestService(
            name=test_name, integration=integration, output_path=output
        )
        test_service.create_test_file()
    except Exception as e:
        print(f"Error creating test: {e}")


# Add the 'run' subcommand
@test_app.command("run")
def run_tests(
    coverage: bool = typer.Option(
        False, "--coverage", "-c", help="Run tests with coverage reporting."
    ),
    report: str = typer.Option(
        None, "--report", "-r", help="Generate a specific report. For example: 'html'."
    ),
):
    """
    Run tests, optionally with coverage and report generation.
    """
    try:
        # Run tests using TestService
        test_service = TestService(coverage=coverage, report=report)
        test_service.run_tests()
    except Exception as e:
        print(f"Error running tests: {e}")


@app.command("init", help="Initialize a new serverless project.")
def app_create(
    project_name: str,
    headless: bool = typer.Option(True, "--headless", help="Run in headless mode."),
):
    try:
        creator = ApplicationService(project_name, headless=headless)
        creator.create_app()
    except Exception as e:
        print(f"Error initializing serverless project: {e}")


@app.command(
    "inspire",
    help="Displays a random inspirational quote and its author for the Spartan like you.",
)
def inspire_display():
    try:
        inspiration_service = InspireService()
        quote = inspiration_service.get_random_quote()
        typer.echo(quote)
    except Exception as e:
        print(f"Error displaying inspirational quote: {e}")


@request_app.command("create", help="Create a new request class.")
def request_create(name: str):
    try:
        service = RequestService(name)
        service.create_request_file()
    except Exception as e:
        print(f"Error creating request: {e}")


@request_app.command("delete", help="Delete an existing request class.")
def request_delete(name: str):
    try:
        service = RequestService(name)
        service.delete_request_file()
    except Exception as e:
        print(f"Error deleting request: {e}")


@response_app.command("create", help="Create a new response class.")
def response_create(name: str):
    try:
        service = ResponseService(name)
        service.create_response_file()
    except Exception as e:
        print(f"Error creating response: {e}")


@response_app.command("delete", help="Delete an existing response class.")
def response_delete(name: str):
    try:
        service = ResponseService(name)
        service.delete_response_file()
    except Exception as e:
        print(f"Error deleting response: {e}")


@infra_app.command("sqs", help="Add sqs service.")
def create_sqs(
    name: str = typer.Argument(..., help="Name of the SQS queue."),
    type: str = typer.Option(
        "standard", help="Type of the SQS queue (standard or fifo).", show_default=True
    ),
    dlq: bool = typer.Option(False, help="Create a Dead Letter Queue (DLQ)."),
):
    try:
        infra_service = InfrastructureService()
        name = infra_service.create_sqs_queue(
            queue_type="sqs", name=name, type=type, dlq=dlq
        )
        typer.echo(f"Queue '{name}' created successfully with sqs type '{type}'.")
    except Exception as e:
        print(f"Error creating SQS queue: {e}")


@infra_app.command("dlq", help="Add dlq service")
def create_dlq(
    name: str = typer.Argument(..., help="Name of the DLQ (Dead Letter Queue)."),
    type: str = typer.Option(
        "standard", help="Type of the SQS queue (standard or fifo).", show_default=True
    ),
):
    try:
        infra_service = InfrastructureService()
        name = infra_service.create_sqs_queue("dlq", name, type)
        typer.echo(f"Queue '{name}' created successfully with sqs type '{type}'.")
    except Exception as e:
        print(f"Error creating DLQ: {e}")


@layer_app.command("build", help="Pull packages and compress it.")
def layer_create(
    requirements_file: Optional[str] = typer.Option(
        "requirements.txt", "--reqs", "-r", help="Path to the requirements file."
    ),
    venv: Optional[str] = typer.Option(
        ".venv/lib", "--env", "-e", help="Path to the virtual environment lib."
    ),
    name: Optional[str] = typer.Option(
        "spartan_lambda_layer", "--name", "-n", help="Name of the layer."
    ),
):
    try:
        layer_service = LayerService(requirements_file, venv, name)
        layer_service.build_layer()
    except Exception as e:
        print(f"Error creating layer: {e}")


if __name__ == "__main__":
    app()
