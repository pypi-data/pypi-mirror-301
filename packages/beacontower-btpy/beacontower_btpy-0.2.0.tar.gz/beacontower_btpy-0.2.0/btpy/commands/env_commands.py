import asyncio

from cyclopts import App
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from btpy.core.envs import env_desc_loader
from btpy.core.envs.env_client import EnvClient
from btpy.core.envs.env_desc_loader import load_env_version, load_env_desc
from btpy.core.envs.env_migrator import migrate_env
from btpy.print_utility import print_status

app = App()


@app.command(name="list")
async def list_envs_cmd():
    env_list = await env_desc_loader.list_envs()

    for env in env_list:
        print(env)


@app.command(name="version")
async def env_version_cmd(env_name: str):
    try:
        version = await load_env_version(env_name)
        print(version)
    except Exception as e:
        print(e)


@app.command(name="status")
async def env_status_cmd(env_name: str):
    try:
        env_desc = await env_desc_loader.load_env_desc(env_name)

        if env_desc is None:
            print("Env not found")
            return
    except Exception as e:
        print(e)
        return

    env_client = EnvClient(env_desc)
    resource_clients = env_client.get_resource_clients()

    with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            TextColumn("{task.fields[result]}"),
    ) as table:
        loop = asyncio.get_event_loop()
        tasks = [
            (
                resource_client,
                loop.create_task(_get_formatted_status(resource_client.client)),
                table.add_task(f"[blue]{resource_client.name}[/blue]", result=""),
            )
            for resource_client in resource_clients
        ]

        while not table.finished:
            for resource_client, task, table_task in tasks:
                if task.done():
                    table.update(
                        table_task, total=100, completed=100, result=task.result()
                    )

            await asyncio.sleep(0.1)

    [await resource_client.client.close() for resource_client in resource_clients]


@app.command(name="upgrade")
async def upgrade_env_cmd(env_name: str, to_version: str):
    await migrate_env(env_name, to_version)


async def _get_formatted_status(resource_client):
    status = await resource_client.status()
    return print_status(status)
