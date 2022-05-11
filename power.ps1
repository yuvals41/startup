##########################WSL#######################################

wsl --install

######################DOCKER########################################

Invoke-WebRequest -OutFile 'C:\Users\user\local-dev-resources\Docker%20Desktop%20Installer.exe' \
-Uri 'https://desktop.docker.com/win/main/amd64/Docker-Desktop-Installer.exe' -UseBasicParsing

##########################MINIKUBE###################################

New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force
Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing

$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){ `
  [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine) `
}

###########################HELM#####################################

choco install -y kubernetes-helm

#########################SKAFFOLD###################################

choco install -y skaffold

############################AWS#####################################

choco install -y awscli

