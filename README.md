# Usage

The kickstart script is to be called thus:

*python -u "path/to/kickstart.py" --job-path "<desired/location/of/the/job>"*

Ensure a valid GitHub access token is saved as an environment variable with alias _"GIT_ACCESS_TOKEN"_.


## How to set up if you want it easier, run as cmd as admin:
1. *copy "path\to\kickstart.py" "c:\"* (or wherever safer you want it)
2. *notepad $PROFILE*
3. add this line to the file: *function kickstart {python -u "c:\kickstart.py" --job-path $args[0]}*
4. save and close
5. restart PowerShell
6. run *"kickstart Folder"*
The folder is a folder name or path.

A folder called "Projects" must exist in your home directory. where it does not exist, it will be created.

Note: You may need to enable script execution in PowerShell. You can do this by opening an elevated PowerShell session (Run as Administrator) and running the following command:
*Set-ExecutionPolicy RemoteSigned*
