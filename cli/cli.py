#!/usr/bin/env python
# TODO: add output flag for human readable or JSON, example in get function

from time import sleep
import click
import json
import requests
import traceback
import os
from pprint import pprint

global_url = "https://discord.com/api/v8/applications/{application_id}/commands"
guild_url = "https://discord.com/api/v8/applications/{application_id}/guilds/{guild_id}/commands"
global_command_url = (
    "https://discord.com/api/v8/applications/{application_id}/commands/{command_id}"
)
guild_command_url = "https://discord.com/api/v8/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"
permission_url = "https://discord.com/api/v8/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions"


@click.group()
def cli():
    "Tool for creating Discord Slash commands."


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.argument("command_file", type=click.STRING)
@click.option(
    "--guild_id",
    type=click.INT,
    help="The Guild ID for the command. Ommit to make a global command.",
)
def post(application_id, bot_token, command_file, guild_id=None):
    with open(f"json_commands/{command_file}", "r") as command_json:
        headers = {"Authorization": f"Bot {bot_token}"}
        try:
            if guild_id:
                url = guild_url.format(application_id=application_id, guild_id=guild_id)
            else:
                url = global_url.format(application_id=application_id)

            r = requests.post(
                url, headers=headers, json=json.loads(command_json.read())
            )
            pprint(r.json())
        except:
            print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.option(
    "--guild_id",
    type=click.INT,
    help="The Guild ID for the command. Ommit to make a global command.",
)
def get(application_id, bot_token, guild_id=None):
    headers = {"Authorization": f"Bot {bot_token}"}
    try:
        if guild_id:
            url = guild_url.format(application_id=application_id, guild_id=guild_id)
        else:
            url = global_url.format(application_id=application_id)

        r = requests.get(url, headers=headers)
        # pprint(r.json())
        print(json.dumps(r.json()))
    except:
        print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("command_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.option(
    "--guild_id",
    type=click.INT,
    help="The Guild ID for the command. Ommit to make a global command.",
)
def delete(application_id, command_id, bot_token, guild_id=None):
    headers = {"Authorization": f"Bot {bot_token}"}
    try:
        if guild_id:
            url = guild_command_url.format(
                application_id=application_id, command_id=command_id, guild_id=guild_id
            )
        else:
            url = global_command_url.format(
                application_id=application_id, command_id=command_id
            )

        r = requests.delete(url, headers=headers)
        print(r.status_code)
    except:
        print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("command_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.argument("command_file", type=click.STRING)
@click.option(
    "--guild_id",
    type=click.INT,
    help="The Guild ID for the command. Ommit to make a global command.",
)
def patch(application_id, command_id, bot_token, command_file, guild_id=None):
    with open(f"json_commands/{command_file}", "r") as command_json:
        headers = {"Authorization": f"Bot {bot_token}"}
        try:
            if guild_id:
                url = guild_command_url.format(
                    application_id=application_id,
                    command_id=command_id,
                    guild_id=guild_id,
                )
            else:
                url = global_command_url.format(
                    application_id=application_id,
                    command_id=command_id,
                    guild_id=guild_id,
                )

            r = requests.patch(
                url, headers=headers, json=json.loads(command_json.read())
            )
            pprint(r.json())
        except:
            print(traceback.format_exc())


# ref: https://discord.com/developers/docs/interactions/slash-commands#get-guild-application-command-permissions
@cli.command()
@click.argument("guild_id", type=click.INT)
@click.argument("application_id", type=click.INT)
@click.argument("command_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.argument("permission_file", type=click.STRING)
@click.option(
    "--disable",
    is_flag=True,
    help="Disable the command for everyone in the Guild",
)
def permission(
    guild_id, application_id, command_id, bot_token, permission_file, disable
):
    if disable:
        disable_json = {
            "permissions": [{"id": guild_id, "type": 1, "permission": False}]
        }

        headers = {"Authorization": f"Bot {bot_token}"}
        try:
            url = permission_url.format(
                application_id=application_id,
                command_id=command_id,
                guild_id=guild_id,
            )
            r = requests.put(url, headers=headers, json=disable_json)
            pprint(r.json())
        except:
            print(traceback.format_exc())

    else:
        with open(f"json_permissions/{permission_file}", "r") as command_json:
            headers = {"Authorization": f"Bot {bot_token}"}
            try:
                url = permission_url.format(
                    application_id=application_id,
                    command_id=command_id,
                    guild_id=guild_id,
                )
                r = requests.put(
                    url, headers=headers, json=json.loads(command_json.read())
                )
                pprint(r.json())
            except:
                print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.option(
    "--guild_id",
    type=click.INT,
    help="The Guild ID for the command. Ommit to make a global command.",
)
def reset(application_id, bot_token, guild_id=None):
    headers = {"Authorization": f"Bot {bot_token}"}
    try:
        if guild_id:
            url = guild_url.format(application_id=application_id, guild_id=guild_id)
        else:
            url = global_url.format(application_id=application_id)

        command_list = requests.get(url, headers=headers).json()

        for command in command_list:
            if guild_id:
                url = guild_command_url.format(
                    application_id=application_id,
                    command_id=command["id"],
                    guild_id=guild_id,
                )
            else:
                url = global_command_url.format(
                    application_id=application_id, command_id=command["id"]
                )

            r = requests.delete(url, headers=headers)
            print(f"[{r.status_code}] {command['id']}: {command['name']}")
            sleep(5)

    except:
        print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.option(
    "--guild_id",
    type=click.INT,
    help="The Guild ID for the command. Ommit to make a global command.",
)
def bulkadd(application_id, bot_token, guild_id=None):
    headers = {"Authorization": f"Bot {bot_token}"}

    if guild_id:
        command_directory = os.fsencode("json_commands/management")
    else:
        command_directory = os.fsencode("json_commands/global")

    # bulk create all commands
    for file in os.listdir(command_directory):
        filename = os.fsdecode(file)

        with open(f"{os.fsdecode(command_directory)}/{filename}", "r") as command_json:
            try:
                if guild_id:
                    url = guild_url.format(
                        application_id=application_id, guild_id=guild_id
                    )
                else:
                    url = global_url.format(application_id=application_id)

                create_command = requests.post(
                    url, headers=headers, json=json.loads(command_json.read())
                )

                print(
                    f"create: [{create_command.status_code}] - command: {create_command.json()['name']}"
                )
                sleep(4)

            except:
                print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.argument("permission_file", type=click.STRING)
@click.option(
    "--guild_id",
    type=click.INT,
    help="The Guild ID for the command. Ommit to make a global command.",
)
def bulkaddwithpermission(application_id, bot_token, permission_file, guild_id=None):
    headers = {"Authorization": f"Bot {bot_token}"}

    if guild_id:
        command_directory = os.fsencode("json_commands/management")
    else:
        command_directory = os.fsencode("json_commands/global")

    # bulk create all commands
    for file in os.listdir(command_directory):
        filename = os.fsdecode(file)

        with open(
            f"{os.fsdecode(command_directory)}/{filename}", "r"
        ) as command_json, open(
            f"json_permissions/{permission_file}"
        ) as permission_json:
            try:
                if guild_id:
                    url = guild_url.format(
                        application_id=application_id, guild_id=guild_id
                    )
                else:
                    url = global_url.format(application_id=application_id)

                create_command = requests.post(
                    url, headers=headers, json=json.loads(command_json.read())
                )

                # add the permission to the role
                url = permission_url.format(
                    application_id=application_id,
                    command_id=create_command.json()["id"],
                    guild_id=guild_id,
                )
                set_permissions = requests.put(
                    url, headers=headers, json=json.loads(permission_json.read())
                )
                print(
                    f"create/permission: [{create_command.status_code}]/[{set_permissions.status_code}] - command: {create_command.json()['name']}"
                )
                print(
                    f"create: [{create_command.status_code}] - command: {create_command.json()['name']}"
                )
                sleep(4)

            except:
                print(traceback.format_exc())


if __name__ == "__main__":
    cli()
