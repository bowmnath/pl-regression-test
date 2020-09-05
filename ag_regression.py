#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess



parser = argparse.ArgumentParser(description=('Regression tests for PL '
                                              'externally-graded questions'))
parser.add_argument('question', type=str, nargs='?', default=os.getcwd(),
                    help=('Directory containing externally-graded question '
                          'to test. Defaults to current working directory'))
parser.add_argument('--tests', nargs='+', metavar='test', dest='test_list',
                    help=('Directories containing specific tests to run. '
                          'If argument is omitted, all tests in '
                          'question/regression_tests will be run'))
args = parser.parse_args()

# Set up path names
course_root = '/home/nate/452/452-pl/'  # TODO
server_files_course = os.path.join(course_root, 'serverFilesCourse')
jobs_dir = os.path.join(course_root, 'pl_tests')
base_workspace_dir = os.path.join(jobs_dir, 'ag_workspace')
base_results_dir = os.path.join(jobs_dir, 'ag_test_results')
question_dir = os.path.abspath(args.question)
regression_dir = os.path.join(question_dir, 'regression_tests')

# Create base directories
os.makedirs(base_workspace_dir, exist_ok=True)
os.makedirs(base_results_dir, exist_ok=True)

# Read external grader environment
info_file_name = os.path.join(question_dir, 'info.json')
with open(info_file_name, 'r') as info_file:
    info = json.load(info_file)
docker_image = info['externalGradingOptions']['image']
entrypoint = info['externalGradingOptions']['entrypoint']
server_files_list = info['externalGradingOptions'].get('serverFilesCourse', [])

# Choose regression test(s) to run
if args.test_list is not None:
    all_tests = args.test_list
else:
    all_tests = os.listdir(regression_dir)

# Run regression tests
success_total = 0
failure_total = 0
for i, submission_name in enumerate(all_tests):

    submission_dir = os.path.join(regression_dir, submission_name)

    # Determine available job_dir
    jobs_in_workspace = os.listdir(base_workspace_dir)
    jobs_in_results = os.listdir(base_results_dir)
    max_job_in_workspace = max([int(s[3:]) for s in jobs_in_workspace],
                               default=1)
    max_job_in_results = max([int(s[3:]) for s in jobs_in_results], default=1)
    job_dir = 'run%d' % (max(max_job_in_workspace, max_job_in_results) + 1)

    workspace_dir = os.path.join(base_workspace_dir, job_dir)
    results_dir = os.path.join(base_results_dir, job_dir)
    server_files_workspace = os.path.join(workspace_dir, 'serverFilesCourse')

    # Create workspace and results directories, creating base directories if
    # they do not exist
    os.makedirs(workspace_dir)
    os.makedirs(results_dir)
    os.makedirs(server_files_workspace)

    # Copy local files into workspace for use by Docker
    shutil.copytree(os.path.join(question_dir, 'tests'),
                    os.path.join(workspace_dir, 'tests'))
    shutil.copytree(submission_dir,
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

    # Compare json output to expected output
    reference_json_name = os.path.join(submission_dir, 'results.json')
    current_json_name = os.path.join(results_dir, 'results.json')

    with open(reference_json_name, 'r') as reference_json:
        reference = json.load(reference_json)
    with open(current_json_name, 'r') as current_json:
        current = json.load(current_json)

    if reference == current:
        success_total += 1
    else:
        print('Test failed. (%s)' % submission_name)
        print('Expected results.json:')
        print(reference)
        print('Observed results.json:')
        print(current)
        failure_total += 1
        if i < len(all_tests) - 1:
            print('\n\n')

print('Total of %d tests run: %d success(es) and %d failure(s).' %
      (len(all_tests), success_total, failure_total))
