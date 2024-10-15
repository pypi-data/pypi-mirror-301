import click

from anc.cli.util import click_group
from anc.api.connection import Connection
#from ac.conf.remote import remote_server, remote_storage_prefix
from pprint import pprint
from tabulate import tabulate
import os
import sys
import json
from requests.exceptions import RequestException
from .util import is_valid_source_path, get_file_or_folder_name, convert_to_absolute_path
from anc.conf.remote import remote_server
from .dataset_operator import DatasetOperator
from .util import get_enviroment


@click_group()
def ds():
    pass


@ds.command()
@click.option("--source_path", "-s", type=str, help="Source path ot the dataset", required=True)
@click.option("--version", "-v", type=str, help="Dataset version you want to register", required=True)
@click.option("--message", "-m", type=str, help="Note of the dataset")
@click.pass_context
def add(ctx, source_path, version, message):
    op = DatasetOperator()
    op.remote_add(version, source_path, message)

@ds.command()
@click.option("--name", "-n", help="Name of the datasets in remote",)
def list(name):
    op = DatasetOperator()
    op.list_dataset(name)


@ds.command()
@click.option("--name", "-n", help="Name of the datasets in remote", required=True)
@click.option("--version", "-v", help="Version of the dataset")
@click.option("--dest", "-d", help="Destination path you want to creat the dataset")
@click.option("--cache_policy", "-c", help="If input is `no` which means no cache used, the dataset will be a completely copy")
@click.pass_context
def get(ctx, name, version, dest, cache_policy):
    op = DatasetOperator()
    op.download_dataset(name, version, dest, cache_policy)


@ds.group()
def queue():
    """Commands for queue operations"""
    pass

@queue.command()
def status():
    """Check the status of the queue"""
    try:
        conn = Connection(url=remote_server)
        response = conn.get("/queue_status")
        
        if 200 <= response.status_code < 300:
            status_data = response.json()
            print("Queue Status:")
            print(json.dumps(status_data, indent=2))
        else:
            print(f"Error: Server responded with status code {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

@ds.group()
def task():
    """Commands for task operations"""
    pass

@task.command()
@click.argument("task_id", type=int)
def status(task_id):
    """Check the status of a task"""
    try:
        conn = Connection(url=remote_server)
        response = conn.get(f"/task_status/{task_id}")
        
        if 200 <= response.status_code < 300:
            status_data = response.json()
            print("Task Status for ID {}:".format(status_data['task_id']))
            print(json.dumps(status_data, indent=2))
        else:
            print(f"Error: Server responded with status code {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")


@task.command()
@click.argument("task_id", type=int)
@click.option("--new-priority", type=int, required=True, help="New priority value for the task")
def increase_priority(task_id, new_priority):
    """Set a new priority for a task"""
    try:
        conn = Connection(url=remote_server)
        data = {"new_priority": new_priority}
        response = conn.post(f"/task/{task_id}/increase_priority", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(result["message"])
        elif response.status_code == 400:
            error = response.json()
            print(f"Error: {error['error']}")
        elif response.status_code == 404:
            error = response.json()
            print(f"Error: {error['error']}")
        else:
            print(f"Error: Server responded with status code {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")


def add_command(cli_group):
    cli_group.add_command(ds)


