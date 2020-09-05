#!/bin/bash

course_root=/home/nate/452/452-pl/
regression_dir=`pwd`/regression_tests/
base_workspace_dir=${regression_dir}/ag_workspace/
base_results_dir=${regression_dir}/ag_test_results/
submission_dir=${regression_dir}/submissions/
job_dir=run2/  # TODO

workspace_dir=${base_workspace_dir}/${job_dir}
results_dir=${base_results_dir}/${job_dir}

mkdir ${workspace_dir}
mkdir ${results_dir}

cp -r tests ${workspace_dir}/tests
cp -r ${submission_dir}/sample ${workspace_dir}/student
cp -r ${course_root}/serverFilesCourse ${workspace_dir}/serverFilesCourse

docker run -it --rm \
    -v ${workspace_dir}:/grade \
    -v ${results_dir}:/grade/results \
    eecarrier/c-and-python-v2 /grade/serverFilesCourse/python_autograder/run.sh
