#! /usr/bin/env python3

import os, sys, re, fileinput

"""
Main test to see if PS1 has been initalized while taking the input from the user and storing it
as a variable that is passed to the input_handler.
"""
def main():
    while True:
        if 'PS1' in os.environ: # check to see if PS1 has been initialized.
            os.write(1, os.environ['PS1'].encode())
        else:
            user_input = input('$ ')
        try:
            user_input = input()
        except EOFError:
            sys.exit(1)

        input_handler(user_input)
"""
Input_handler designates what method will be called based on user_input.

"""

def input_handler(user_input):

    args = user_input.split()

    if user_input == "":
        pass
    
    elif 'exit' in user_input:
        sys.exit(0)
        
    elif '|' in user_input:
        pipe_handler(user_input)        
        
    elif 'cd' in user_input:
        try:
            os.chdir(args[1].strip())
        except FileNotFoundError:
            pass
    else:
        execute_command(args)
"""
Pipe_handler takes in user input as a pramter. It then parses the input for two sperate commands.
(Currently not working properly)

"""
            
def pipe_handler(user_input):
    # child fork / creates a new process
    rc = os.fork()

    args = user_input.split('|')

    if rc < 0:
        sys.exit(1)

    elif rc == 0:
        pr, pw = os.pipe()
        for f in (pr, pw):
            os.set_inheritable(f, True)
        
        pf = os.fork()
        
        if pf < 0:                      # fork failed   
            sys.exit(1)
    
        elif pf == 0:                   #  child - will write to pipe
            os.close(1)                 #  redirect child's stdout
            os.dup(pw)
            os.set_inheritable(1,True)
            
            for fd in (pr,pw):    
                os.close(fd)                    
                print("\nhello from child\n")
            execute_command(args[0].strip())
                
        else:                           # parent (for
            os.close(0)
            os.dup(pr)
            os.set_inheritable(0,True)
            for fd in (pw,pr):
                os.close(fd)
                print("From child: <%s>" % line)
            execute_command(args[1].strip())
    
    else:                           # parent (forked ok)
        childPidCode = os.wait()
"""
Execute_command takes a pre parsed input that check to see if it is a redirect if so depending on
the symbol it will either read from the last or create and write a new file. Followed by executing
the the user input while traversing through the 'PATH' 

"""        
def execute_command(args):
    pid = os.getpid()
    
    rc = os.fork()

    if rc < 0:
        sys.exit(1)

    elif rc == 0:
        if '>' in args or '<' in args:
            if '>' in args:
                args.remove(">")
                os.close(1)
                os.open(args[-1], os.O_CREAT | os.O_WRONLY);
                os.set_inheritable(1, True)
            else:
                os.close(0)
                sys.stdin = open(args[-1], 'r')
                os.set_inheritable(0, True)
        
        # Get path Variable and splits it by the : which will provide individual paths.
        # For each directory on the path we will walk though it and try to execve the program
        # pointed to the filename            
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Could not execute %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error


        
if __name__=="__main__":
    main()
