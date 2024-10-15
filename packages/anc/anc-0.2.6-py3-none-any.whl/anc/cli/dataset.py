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
    project, cluster = get_enviroment()
    source_path = os.path.abspath(source_path)
    if not is_valid_source_path(source_path):
        sys.exit(1) 
    abs_path = convert_to_absolute_path(source_path)
    dataset_name = get_file_or_folder_name(abs_path)
    conn = Connection(url=remote_server)
    data = {
        "dataset_name": dataset_name,
        "version": version,
        "source_path": abs_path,
        "dest_path": "local",
        "project": project,
        'cluster': cluster,
        "message": message
    }
    try:
        response = conn.post("/add", json=data)
        
        # Check if the status code is in the 2xx range
        if 200 <= response.status_code < 300:
            response_data = response.json()
            task_id = response_data.get('task_id')
            if task_id:
                print(f"Task added successfully. Your task ID is: {task_id}")
                print(f"You can check the status later by running: anc ds list -n {dataset_name}")
            else:
                print("Task added successfully, but no task ID was returned.")
        else:
            print(f"Error: Server responded with status code {response.status_code}")
            print(f"{response.text}")
            
    except RequestException as e:
        print(f"Error occurred while communicating with the server: {e}")
    except json.JSONDecodeError:
        print("Error: Received invalid JSON response from server")
    except KeyboardInterrupt:
        print(f"Operation interrupted. The dataset add operation may still be processing on the backend.")
        print(f"You can check its status later by running: anc ds list -n {dataset_name} -v {version}")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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
            print(f"Task Status for ID {task_id}:")
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


