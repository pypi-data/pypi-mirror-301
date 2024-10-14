import os
import argparse
from scientiflow_cli.cli.login import login_user#, user_has_auth_token, get_auth_token
from scientiflow_cli.cli.login import login_user
from scientiflow_cli.cli.logout import logout_user
from scientiflow_cli.pipeline.get_jobs import get_jobs
from scientiflow_cli.utils.file_manager import create_job_dirs, get_job_files
from scientiflow_cli.pipeline.container_manager import get_job_containers
from scientiflow_cli.utils.mock import mock_jobs
from scientiflow_cli.services.executor import execute_jobs
from scientiflow_cli.cli.auth_utils import getAuthToken


AUTH_TOKEN = os.getenv("AUTH_TOKEN", None)

def main():
    parser = argparse.ArgumentParser(description="Scientiflow Agent CLI")

    parser.add_argument('--login', action='store_true', help="Login using your scientiflow credentials")
    parser.add_argument('--logout', action='store_true', help="Logout from scientiflow")
    # parser.add_argument('--list-jobs', action='store_true', help="Get jobs to execute")
    parser.add_argument('--get-files', action='store_true', help="Get user files")
    parser.add_argument('--get-containers', action='store_true', help="Download containers for the user")
    parser.add_argument('--mock-pipeline-decode', action='store_true', help="Decode the mock pipeline")
    parser.add_argument('--execute-jobs', action='store_true', help="Fetch and execute pending jobs")
    args = parser.parse_args()


    try:
        # We're checking here that if command is either login or logout, then we don't need to check for auth token
        # since these two are the only two commands allowed to run without an auth token
        # if not args.login and not args.logout:
        #     print("Session not found. Please login to continue")
        #     return
        if args.login:
            login_user()
        
        elif args.logout:
            logout_user()
        # elif args.list_jobs:
        #     get_jobs(auth_token = getAuthToken())

        elif args.get_files:
            get_job_files(auth_token = AUTH_TOKEN)
        elif args.get_containers:
            get_job_containers(auth_token = AUTH_TOKEN)

        # This is a mock pipeline decode. This is used to test the functions that are used to decode the pipeline
        # elif args.mock_pipeline_decode:
        #     for job in mock_jobs:
        #         create_job_dirs(job)
        #         get_job_files(auth_token = AUTH_TOKEN, job = job)
        #         get_job_containers(auth_token = AUTH_TOKEN, job = job)

        elif args.execute_jobs:
            execute_jobs(auth_token=getAuthToken())
        else:
            print("No arguments specified. Use --help to see available options")
    
    except Exception as e:
        print("Error: ", e)
        return


if __name__ == "__main__":
    main()