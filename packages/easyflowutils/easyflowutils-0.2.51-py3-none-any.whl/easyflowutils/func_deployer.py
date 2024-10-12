import os
import subprocess
import getpass


def deploy_func(func_name, region="europe-west9", source="."):
    try:
        subprocess.run("gcloud auth print-access-token", shell=True, check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("You are not logged in to gcloud. Please provide your OAuth 2.0 token.")
        token = getpass.getpass("Enter your token: ")
        subprocess.run(f"gcloud auth activate-service-account --key-file={token}", shell=True, check=True)

    os.chdir(os.path.abspath(source))

    command = (
        f"gcloud functions deploy {func_name} "
        f"--gen2 "
        f"--runtime=python312 "
        f"--region={region} "
        f"--source={source} "
        f"--entry-point={func_name} "
        f"--trigger-http "
        f"--allow-unauthenticated"
    )
    subprocess.run(command, shell=True, check=True)
