from concurrent.futures import ThreadPoolExecutor
import asyncio
import os

from scientiflow_cli.pipeline.get_jobs import get_jobs
from scientiflow_cli.pipeline.decode_and_execute import decode_and_execute_pipeline
from scientiflow_cli.pipeline.container_manager import get_job_containers
from scientiflow_cli.utils.file_manager import create_job_dirs, get_job_files


def get_all_pending_jobs(auth_token: str) -> list[dict]:
    """
    Gets all the pending jobs using the get_jobs function
    """
    try:
        return get_jobs(auth_token)

    except Exception as e:
        print("An unexpected error occurred")
        return []


def execute_jobs(auth_token: str) -> None:
    """
    Starts the execute_jobs coroutine
    """
    asyncio.run(execute(auth_token))


async def execute(auth_token: str) -> None:
    """Executes the function 'execute_job' asynchronously.
       Since synchronous functions do not run in a non blocking way, to achieve that
       each job is being executed on a seperate thread"""
    
    # Retrieve all jobs using 'get_jobs'
    all_pending_jobs: list[dict] = []
    
    all_pending_jobs = get_all_pending_jobs(auth_token)
    
    running_jobs: list[asyncio.Future] = []  # List of all running jobs
    loop = asyncio.get_running_loop()  # Get the current running event loop

    with ThreadPoolExecutor() as exec:
        for job in all_pending_jobs:

            # Running 'decode_and_execute_job' in a separate thread
            task = loop.run_in_executor(exec, execute_single_job, auth_token, job)
            running_jobs.append(task)

        await asyncio.gather(*running_jobs)  # Wait for all running jobs to complete


def execute_single_job(auth_token: str, job: dict) -> None:

    """Function to decode and execute a job. Currently does nothing.
        Processes a job asynchronously but maintains synchronous 
        execution of the internal logic. Note: Terminal outputs will not be in order
        since multiple jobs are running simultaneously
       
       Raises:
           ValueError: If the job is missing required fields.
           RuntimeError: If the job fails during runtime
    """
    try:
        # Validate the job dictionary
        required_keys = ["server", "project", "project_job", "nodes", "edges", "new_job"]

        for key in required_keys:
            if key not in job:
                raise ValueError(f"Job is missing required key: {key}")
            

        # Store all the variables with their types

        base_dir: str = job['server']['base_directory']
        project_job_id: int = job['project']['id']
        project_title: str = job['project']['project_title']
        job_dir_name: str = job['project_job']['job_directory']
        nodes: list[dict] = job['nodes']
        edges: list[dict] = job['edges']
        environment_variables_management: list[dict] = job['environment_variable_management']
        environment_variables: dict = {environment_var['variable'] : environment_var['value'] for environment_var in environment_variables_management}

        # Initialize folders for the project / project_job 
        create_job_dirs(job)

        # Fetch the files and folder from the backend
        get_job_files(auth_token, job)

        # Get the job containers from the backend
        get_job_containers(auth_token, job)

        # Decode and execute the pipeline step by step
        decode_and_execute_pipeline(base_dir, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables)



    except ValueError as value_err:
        print(f"ValueError encountered while processing job: {value_err}")

    except RuntimeError as runtime_err:
        print(f"RuntimeError encountered while processing job: {runtime_err}")

    except Exception as err:
        print(f"An unexpected error occurred while processing job: {err}")