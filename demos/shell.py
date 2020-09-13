#! /usr/bin/env python3

import os, sys, time, re


def main():

    while True:
        
        user_input = input(os.getcwd() + ">$ ")
        input_handler(user_input)

"""
Command handler takes in user input as a parameter and checks to see id the command enter is valid.
Otherwise it will prompt that the user should input once again.

"""        
def command_handler(user_input):
    try:
        if os.system(user_input[0]) != 0:
            print(user_input)
            raise Exception()
    except Exception as e:
        print("\nCommand not found! Please Try again.\n")
    finally:
        pass

"""
Some functionaltiy still does not work properly

"""            
def input_handler(user_input):

    args = user_input.split()

    command_handler(args)
    
    if user_input == "":
        pass

    if 'exit' in user_input:
        sys.exit(0)

    if '>' in user_input or '<' in user_input:
        redirect_handler(user_input)

    if '|' in user_input:
        user_input = user_input.split('|')
        for args_input in user_input:
            args = args_input.split()
            command_handler(args)
            execute_command(args)

    if 'cd' in user_input:
        os.chdir(args[1])
        print(os.getcwd())

    else:
        execute_command(args)

        
def redirect_handler(user_input):

    
    if '>' in user_input:
        os.close(1)
        args = user_input.split('>')
        os.open(args[2], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1,True)
        #command_execute(args)
    else:
        os.close(1)
        args = user_input.split('<')
        os.open(args[2], os.O_RDONLY)
        os.set_inheritable(0,True)
        #command_execute(args)
            

def execute_command(args):
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

if __name__=="__main__":
    main()
