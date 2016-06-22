#!/bin/bash

# Runs all the tribe admin commands on the test MBOX for quick testing
# of Python 2 and 3 for the tribe-admin.py script. Note this will be moved
# to the Python unittest framework in admin_script_tests.py

# First change the working directory to the location this script is.
swd=$(cd "$(dirname "${BASH_SOURCE}")"; pwd -P)
cd "$swd"

# First test the help and version command
echo -e "Test the help option:"
python ../tribe-admin.py --help
echo -e "\n--------------------\n"

echo -e "Test the version option:"
python ../tribe-admin.py --version
echo -e "\n--------------------\n"

# Next test the headers command
echo -e "Test the headers command:"
python ../tribe-admin.py headers -w fixtures/headers.json fixtures/test.mbox
echo -e "\n--------------------\n"

# Next test the count command
echo -e "Test the count command:"
python ../tribe-admin.py count fixtures/test.mbox
echo -e "\n--------------------\n"

# Next test the extract command
echo -e "Test the extract command:"
python ../tribe-admin.py extract -w fixtures/test.graphml fixtures/test.mbox
echo -e "\n--------------------\n"

# Next test the info command
echo -e "Test the info command:"
python ../tribe-admin.py info fixtures/test.graphml
echo -e "\n--------------------\n"

# Next test the draw command
echo -e "Test the draw command:"
python ../tribe-admin.py draw -w fixtures/test.png fixtures/test.graphml
echo -e "\n--------------------\n"
