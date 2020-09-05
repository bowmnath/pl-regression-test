#!/bin/bash

course_root=/home/nate/452/452-pl/
regression_dir=`pwd`/regression_tests/
workspace_dir=${regression_dir}/ag_workspace/
submission_dir=${regression_dir}/submissions/
results_dir=${regression_dir}/ag_test_results/
job_dir=run1/  # TODO

cp -r tests ${workspace_dir}/tests
cp -r ${submission_dir}/sample ${workspace_dir}/student
cp -r ${course_root}/serverFilesCourse ${workspace_dir}/serverFilesCourse

docker run -it --rm \
    -v ${workspace_dir}:/grade \
    -v ${results_dir}/${job_dir}:/grade/results \
    eecarrier/c-and-python-v2 /grade/serverFilesCourse/python_autograder/run.sh
