#! /usr/bin/env python3

import os, sys, time, re


while True:
    args = input("$ ")
    args = args.split() 
    print(args)
    if args[0] == 'exit':
        sys.exit(0)
    else:
        # create parents P_rocess ID_entification
        pid = os.getpid()
            
        # child fork / creates a new process
        rc = os.fork()
        
        # Verify that the fork is running
        if rc < 0:
            sys.exit(1)
            
        elif rc == 0: # child
            # Get path Variable and splits it by the : which will provide individual paths.
            # For each directory on the path we will walk though it and try to execve the program
            # pointed to the filename            
            #args = ["wc", "p3-exec.py"]
            for dir in re.split(":", os.environ['PATH']): # try each directory in the path

                program = "%s/%s" % (dir, args[0])
                
                try:
                    os.execve(program, args, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly
                
            os.write(2, ("Could not execute %s\n" % args[0]).encode())
            sys.exit(1)                 # terminate with error
            
        else:                           # parent (forked ok)
            childPidCode = os.wait()
