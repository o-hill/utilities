# Written for Umich EECS 370 by Oliver Hill <oliverhi@umich.edu>

# YOU NEED TO EDIT SEVERAL THINGS IN THIS FILE.
# Firstly, the remote directory.
# Then, in the rsync command, enter the directory in which
#    your project lies.
# You also need to change the uniqname for CAEN login in two places.

# I put this script in the directory that my project is in,
# and then you can run it to submit with the command: "sh submit.sh"
# Let me know if you find any problems or have ideas of what to change!
# You'll have to type your CAEN passowrd twice :(

# Declare your remote directory.  I couldn't figure out the
# syntax for the local directory for some reason, so let me
# know if you do!
# TODO: Change to your CAEN directory.
REMOTEDIR="~/Desktop/eecs370/project4/"

# Sync your local directory with the remote directory.
# TODO: Modify local filepath and uniqname for login.
rsync -av ~/Documents/School/Umich/EECS370/Projects/project4/ oliverhi@login.engin.umich.edu:${REMOTEDIR}

# Declare what part of the project you're working on here.
# TODO: Change to your shit!
PROJPART="4"
EXE="cache.c"

# Add all your test file names here, with ${REMOTEDIR} beforehand.
# Lets concatenate all of the test names with the
# remote file path as well, for convenience later on.
# TODO: Rename tests
TESTS="${REMOTEDIR}spec.as.4.2.1 ${REMOTEDIR}spec.as.1.1.4 ${REMOTEDIR}spec.as.2.8.2"
CMD="/afs/umich.edu/class/eecs370/bin/submit370"

# Concatenate the executable file with the remote file path.
EXE="${REMOTEDIR}${EXE}"

# Print the commands you're running before you type
# your password the second time, so you know what
# you are submitting.
echo "Check your submission!  Control-C if it's wrong\n"
echo "Project part: ${PROJPART}\n"
echo "Executable: ${EXE}\n"
echo "Tests: ${TESTS}\n"

# And we're done!
# TODO: Change uniqname.
ssh oliverhi@login.engin.umich.edu "yes y | ${CMD} ${PROJPART} ${EXE} ${TESTS}"
