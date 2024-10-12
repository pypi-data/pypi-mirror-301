from cyclopts import App
import importlib.metadata

from btpy.commands import env_commands
from btpy.commands import software_commands
from btpy.commands import iac_commands


def get_version():
    return importlib.metadata.version("beacontower-btpy")


app = App(version=get_version)

app.command(env_commands.app, name="env")
app.command(software_commands.app, name="software")
app.command(iac_commands.app, name="iac")

if __name__ == "__main__":
    app()
