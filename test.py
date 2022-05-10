from asyncio.windows_utils import PIPE
import os
import sys
import subprocess

# command = "powershell -Command New-Item -Path 'c:\\' -Name 'minikube' -ItemType Directory -Force"
# command2 = "powershell -Command Invoke-WebRequest -OutFile 'c:\\minikube\\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing"
command3 = "$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)"
command4 = "if($oldPath.Split(';') -inotcontains 'C:\\minikube'){ [Environment]::SetEnvironmentVariable('Path', $('{\0};C:\\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)}"

# command = command.split()

# command2 = command2.split()

command3 = command3.split()

command4 = command4.split()

print(command3)

def run(cmd):
    cmd.insert(0, "-Command")
    cmd.insert(0, "powershell")
    print(cmd)
    output = subprocess.run(cmd,capture_output=True)
    print(output.stdout,output.stderr)


# run(command)
# run(command2)
run(command3)
# run(command4)