#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess



parser = argparse.ArgumentParser(description=('Regression tests for PL '
                                              'externally-graded questions'))
parser.add_argument('base', metavar='base directory', type=str, nargs='?',
                    default=os.getcwd(),
                    help=('Directory containing externally-graded question '
                          'to test. Defaults to current working directory'))
args = parser.parse_args()

# Choose regression test to run
submission_name = 'sample'  # TODO

# Set up path names
course_root = '/home/nate/452/452-pl/'  # TODO
server_files_course = os.path.join(course_root, 'serverFilesCourse')
base = os.path.abspath(args.base)
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
server_files_workspace = os.path.join(workspace_dir, 'serverFilesCourse')

# Create workspace and results directories, creating base directories if
# they do not exist
os.makedirs(workspace_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)
os.makedirs(server_files_workspace)

# Read external grader environment
info_file_name = os.path.join(base, 'info.json')
with open(info_file_name, 'r') as info_file:
    info = json.load(info_file)
docker_image = info['externalGradingOptions']['image']
entrypoint = info['externalGradingOptions']['entrypoint']
server_files_list = info['externalGradingOptions'].get('serverFilesCourse', [])

# Copy local files into workspace for use by Docker
shutil.copytree(os.path.join(base, 'tests'),
                os.path.join(workspace_dir, 'tests'))
shutil.copytree(os.path.join(submission_dir, submission_name),
                os.path.join(workspace_dir, 'student'))
for server_file_rel in server_files_list:
    server_file_abs = os.path.join(server_files_course, server_file_rel)
    dest_file = os.path.join(server_files_workspace, server_file_rel)
    if os.path.isdir(server_file_abs):
        shutil.copytree(server_file_abs, dest_file)
    else:
        shutil.copy(server_file_abs, dest_file)

docker_command = ['docker', 'run', '-it', '--rm',
                  '-v', '%s:/grade' % workspace_dir,
                  '-v', '%s:/grade/results' % results_dir,
                  docker_image, entrypoint]

subprocess.run(docker_command, universal_newlines=True, capture_output=True,
               check=True)
