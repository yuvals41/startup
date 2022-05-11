from genericpath import exists
import os
import sys


# command3 = "$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)"
# command4 = "if($oldPath.Split(';') -inotcontains 'C:\\minikube'){ [Environment]::SetEnvironmentVariable('Path', $('{\0};C:\\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)}"





# print(os.system("wsl --install"))
# print(os.system("powershell -Command New-Item -Path 'c:\\' -Name 'minikube' -ItemType Directory -Force"))
# print(os.system("powershell -Command Invoke-WebRequest -OutFile 'c:\\minikube\\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing"))
# print(os.system("powershell -Command $oldpath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine); if ($oldpath.Split(';') -inotcontains 'C:\minikube') { [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine) }"))

# print(os.system("powershell -Command choco install -y kubernetes-helm"))
# print(os.system("powershell -Command choco install -y skaffold"))
# print(os.system("powershell -Command choco install -y awscli"))

# os.system("powershell -Command Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All")


os.system("powershell -Command if((Get-WindowsOptionalFeature -FeatureName Microsoft-Hyper-V-All -Online).State -ne 'Enabled') { Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All}")


# sys.

# if 'minikube' in os.getenv('Path'):
#     print("yes")

# if 'AWSCLIV2' in os.getenv('Path'):
#     print("yes")

# if 'AWSCLIV2' in os.getenv('Path'):
#     print("yes")

# if exists(r'C:\ProgramData\chocolatey\bin\helm.exe'):
#     print("yes")
