#!/usr/bin/env python3

import os
import shutil
import subprocess



# External grader environment  TODO should not be hard-coded
docker_image = 'eecarrier/c-and-python-v2'
entrypoint = '/grade/serverFilesCourse/python_autograder/run.sh'

# Choose regression test to run
submission_name = 'sample'  # TODO

# Set up path names
course_root = '/home/nate/452/452-pl/'  # TODO
base = os.getcwd()  # TODO accept an argument for base -- default to cwd
regression_dir = os.path.join(base, 'regression_tests')
base_workspace_dir = os.path.join(regression_dir, 'ag_workspace')
base_results_dir = os.path.join(regression_dir, 'ag_test_results')
submission_dir = os.path.join(regression_dir, 'submissions')

# Determine available job_dir
jobs_in_workspace = os.listdir(base_workspace_dir)
jobs_in_results = os.listdir(base_results_dir)
max_job_in_workspace = max([int(s[3:]) for s in jobs_in_workspace])
max_job_in_results = max([int(s[3:]) for s in jobs_in_results])
job_dir = 'run%d' % (max(max_job_in_workspace, max_job_in_results) + 1)

workspace_dir = os.path.join(base_workspace_dir, job_dir)
results_dir = os.path.join(base_results_dir, job_dir)

# Create workspace and results directories, creating base directories if
# they do not exist
os.makedirs(workspace_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# Copy local files into workspace for use by Docker
shutil.copytree(os.path.join(base, 'tests'),
                os.path.join(workspace_dir, 'tests'))
shutil.copytree(os.path.join(submission_dir, submission_name),
                os.path.join(workspace_dir, 'student'))
shutil.copytree(os.path.join(course_root, 'serverFilesCourse'),
                os.path.join(workspace_dir, 'serverFilesCourse'))

docker_command = ['docker', 'run', '-it', '--rm',
                  '-v', '%s:/grade' % workspace_dir,
                  '-v', '%s:/grade/results' % results_dir,
                  docker_image, entrypoint]

subprocess.run(docker_command, universal_newlines=True, capture_output=True,
               check=True)
