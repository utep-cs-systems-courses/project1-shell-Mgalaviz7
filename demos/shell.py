#! /usr/bin/env python3

import os
import sys
import re

#fdOut = os.open("p0-output.txt", os.O_CREAT | os.O_WRONLY)
#fdIn = os.open("shell.py", os.O_RDONLY)

# create parents P_rocess ID_entification
pid = os.getpid() 

os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

# child fork / creates a new process
rc = os.fork()

#os.write(1, ("child fork (pid:%d)\n" % rc).encode())


# Verify that the fork is running
if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child

    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())

    
    args = ["wc", "p3-exec.py"]

# Get path Variable and splits it by the : which will provide individual paths.
# For each directory on the path we will walk though it and try to execve the program
# pointed to the filename

    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly

    os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
