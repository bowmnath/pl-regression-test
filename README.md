Simple script for testing
[PrairieLearn](https://prairielearn.engr.illinois.edu/)
external graders.

**Warning**: this software has not been thoroughly tested.
The code does not do much error checking.
I have experimented with it on my Linux system and not had anything go
catastrophically wrong,
but that is the extent of the testing.

## Purpose

Whenever you make changes to an externally-graded question,
you risk breaking current functionality.
One way to avoid this is to keep around old submissions with known results and
rerun them after updating the autograder.
However, rerunning by hand is tedious,
and this script was designed to automate that process.

## How do you set it up?

First, you will need a set of submissions to the problem (the code) and the
resulting `results.json` file for each submission.
Each (submission, results) pair goes in its own directory.
How you name the directories is up to you,
but I suggest using descriptive names explaining how or why you chose that
test.
As of this writing,
PrairieLearn mandates the name of the code submission,
so you must use that name for all of your code files.

All of these directories containing (submission, results) pairs must be put in a
directory named `regression_tests` that is a subdirectory of the
externally-graded question (`foo`, in our example).
This is what the layout should look like:

```
questions/
    foo/
        info.json
        question.html
        regression_tests/ <-- directory for this project
            expect-to-fail/
                [problem_code].py
                results.json
            full-credit/
                ...
            raises-exception/
                ...
        tests/
```

## How do you start the tests?

Ensure that the file `ag_regression.py` is somewhere in your path and
executable.

You can run `ag_regression.py -h` to see the help message.
Essentially, you point it to the question directory
(`foo/` in our example),
which is assumed to be the current directory if not included,
and it automatically runs all of the tests.
You can also pass the `--tests` argument followed by a space-delimited list of
tests
(such as `expect-to-fail` and `full-credit` in the above example)
to run only those tests.

By default, the script assumes the course root is two directories above the
question.
This will work if your questions are stored "flat" in the questions directory.
If the questions themselves are nested deeper,
you will need to pass the `--course_root` argument with the absolute path of
your course root.
The root directory of your PrairieLearn course is the one with
`infoCourse.json`.
To avoid needing to type this every time,
you may want to make another script for a particular course that calls this
script with the `--course-root` argument hard-coded.

That's it!

## What does the output look like?

Any time there is a mismatch between the stored results and the results
generated by the test,
the program will notify you,
print the test name,
and print the expected `results.json` and the observed `results.json`.
Successes are not printed.
At the end,
the total number of tests, successes, and failures is given.

For example:

```
Test failed. (expect-to-fail)
Expected results.json:
{'tests': [{'name': 'oes it compile?', 'max_points': 4, 'points': 4, 'files': []}, {'name': 'Does your code produce correct output?', 'max_points': 1, 'points': 1, 'files': []}, {'name': 'Have you fixed *all* memory problems?', 'max_points': 4, 'points': 4, 'files': []}], 'score': 1.0, 'succeeded': True, 'max_points': 9}
Observed results.json:
{'tests': [{'name': 'Does it compile?', 'max_points': 4, 'points': 4, 'files': []}, {'name': 'Does your code produce correct output?', 'max_points': 1, 'points': 1, 'files': []}, {'name': 'Have you fixed *all* memory problems?', 'max_points': 4, 'points': 4, 'files': []}], 'score': 1.0, 'succeeded': True, 'max_points': 9}



Total of 2 tests run: 1 success(es) and 1 failure(s).
```

Not the easiest to look at,
but it should help you get started.
