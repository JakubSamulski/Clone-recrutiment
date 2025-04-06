from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import Command as RunserverCommand

from django.conf import settings


class Command(BaseCommand):
    """
    Custom wrapper for the runserver command.

    Allows specifying the host and port directly as an argument,
    e.g., `manage.py myrunserver 0.0.0.0:8080`.
    """

    help = "Runs the development server with an optional host:port argument."

    # We inherit the default_addr and default_port from the original command
    # to ensure consistency if they change in future Django versions.
    default_addr = RunserverCommand.default_addr
    default_port = RunserverCommand.default_port

    def add_arguments(self, parser):
        parser.add_argument(
            "host",
            nargs="?",
            type=str,
            default="localhost",
            help=(
                "Optional host to bind the server to " f"(default: {self.default_addr})"
            ),
        )
        parser.add_argument(
            "port",
            nargs="?",
            type=str,
            default="5478",
            help=(
                "Optional port to bind the server to " f"(default: {self.default_port})"
            ),
        )

        parser.add_argument(
            "log_level",
            nargs="?",  # Makes the argument optional
            type=str,
            default=f"{settings.LOG_LEVEL}",
            help="Optional log level " f"(default: {settings.LOG_LEVEL})",
        )

        parser.add_argument(
            "refresh_rate",
            nargs="?",
            type=str,
            default=f"{settings.REFRESH_RATE}",
            help="Optional refresh rate " f"(default: {settings.REFRESH_RATE})",
        )

    def handle(self, *args, **options):
        """
        Executes the command logic.
        """
        port = options["port"] if options["port"] else self.default_port
        host = options["host"] if options["host"] else self.default_addr
        addrport = f"{host}:{port}"

        self.stdout.write(f"Starting custom development server wrapper...")
        self.stdout.write(f"Binding to address: {addrport}")

        runserver_args = [addrport]
        runserver_options = {}

        try:
            call_command(
                "runserver",
                *runserver_args,
                **runserver_options,
            )
        except KeyboardInterrupt:
            self.stdout.write("Server stopped.")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error running runserver: {e}"))
            # Optionally re-raise or handle differently
            raise
