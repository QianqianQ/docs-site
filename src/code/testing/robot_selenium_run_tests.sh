#!/bin/bash

# clean output files in results directory if 'clean' is entered as first or second parameter
if [ "$1" = "clean" ]  ||  [ "$2" = "clean" ] ||  [ "$3" = "clean" ]; then
    # check to verify results folder exists
    if [ -d "results" ]; then
        rm -r results
    fi
fi

if [ "$1" = "xxx" ]; then
    echo "### xxx Robot tests ###"
    if [ "$2" = "Calculation" ] ||  [ "$2" = "GUI" ]; then
        echo ">> Running xxx tests with '$2' tag"
        # execute all xxx tests with given tag and save output in 'results' folder
        robot --outputdir results -i "$2" tests/xxx.robot
    else
        # execute all xxx tests and save output in 'results' folder
        robot --outputdir results tests/xxx.robot
    fi
else
    echo "### Robot tests ###"
    if [ "$1" = "Calculation" ] ||  [ "$1" = "GUI" ]; then
        echo ">> Running all tests with '$1' tag"
        # execute all tests with given tag and save output in 'results' folder
        robot --outputdir results -i "$1" tests
    else
        # execute all tests and save output in 'results' folder
        robot --outputdir results tests
    fi
fi

# if test fails, re-execute failing tests and save the results in rerun-test-results
if [ $? -eq 1 ]; then
    echo ""
    echo "### Re-run failed tests ###"
    # re-execute failing tests
    if [ "$1" = "xxx" ]; then
        robot --outputdir results/rerun-test-results --rerunfailed results/output.xml tests/xxx.robot
    else
        robot --outputdir results/rerun-test-results --rerunfailed results/output.xml tests
    fi
fi
