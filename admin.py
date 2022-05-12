import os
from os.path import exists
import sys
import subprocess
import typer


def install_deps_windows():

    def choco():
        status = os.system("powershell -Command Set-ExecutionPolicy Bypass -Scope Process -Force; \
         [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; \
          iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")

        if status != 0:
            raise("failed to install choco")

    def wsl():
        status = os.system("choco install wsl2")

        if status != 0:
            raise("failed to install wsl2")

        status = os.system("wsl --set-default-version 2")

        if status != 0:
            raise("failed to set wsl to version 2")
    
    def enable_windows_features():
       status = os.system("powershell -Command if((Get-WindowsOptionalFeature -FeatureName Microsoft-Hyper-V-All -Online).State -ne 'Enabled') \
        { Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All}")
        
       if status != 0:
            raise("failed to enable hyperv")

       status = os.system("powershell -Command dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart")
        
       if status != 0:
            raise("failed to enable windows subsystem for linux")

       status = os.system("powershell -Command dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart")
        
       if status != 0:
            raise("failed to enable virtual machine platform")
    
    def docker():
        status = os.system("choco install -y docker-desktop")

        if status != 0:
            raise("failed to install docker")

    def minikube():
        status = os.system("powershell -Command New-Item -Path 'c:\\' -Name 'minikube' -ItemType Directory -Force")
        if status != 0:
            raise("failed to create directory")

        status = os.system("powershell -Command Invoke-WebRequest -OutFile 'c:\\minikube\\minikube.exe' \
        -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing")

        if status != 0:
            raise("failed to install minikube")

        status = os.system("powershell -Command $oldpath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine); \
        if ($oldpath.Split(';') -inotcontains 'C:\minikube') { [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), \
        [EnvironmentVariableTarget]::Machine) }")

        if status != 0:
            raise("failed to add minikube to path")

    def helm():

        status = os.system("powershell -Command choco install -y kubernetes-helm")

        if status != 0:
            raise("failed to install helm")
    
    def skaffold():

        status = os.system("powershell -Command choco install -y skaffold")

        if status != 0:
            raise("failed to install skaffold")

    def aws_cli():
        status = os.system("powershell -Command choco install -y awscli")

        if status != 0:
            raise("failed to install aws cli")

    #checks if choco exists
    if not exists(r'C:\ProgramData\chocolatey\bin'):
        choco()

    #enables important features for docker
    enable_windows_features()

    #set the wsl version to 2
    if not exists(r'C:\ProgramData\chocolatey\lib\wsl2'):
        wsl()

    #checks if Docker exists
    if not exists(r'C:\Program Files\Docker\Docker\resources\bin\docker.exe'):
        docker()

    #checks if minikube exists
    if not exists(r'c:\minikube\minikube.exe'):
        minikube()

    #checks if aws exists
    if not exists(r'C:\Program Files\Amazon\AWSCLIV2\aws.exe'):
        aws_cli()

    #checks if helm exists
    if not exists(r'C:\ProgramData\chocolatey\bin\helm.exe'):
        helm()
        
    #checks if skaffold exists
    if not exists(r'C:\ProgramData\chocolatey\bin\skaffold.exe'):
        skaffold()


def deploy_windows(dir, dump_file_path):

    def create_namespace():
        status = os.system("powershell -Command kubectl create namespace attack; \
                             kubectl create namespace cymulate; \
                             kubectl create namespace recon")

        if status != 0:
            raise("failed to create namespace")

    def redis_install():
        status = os.system("powershell -Command helm repo add bitnami https://charts.bitnami.com/bitnami; \
                             helm repo update; \
                             helm upgrade --install -n cymulate --set cluster.enabled=false --set auth.enabled=false --set master.command=\"\" \
                            --set image.repository=redis --set image.tag=6.0 --set master.disableCommands="" --set replica.replicaCount=0 \
                            --set master.containerSecurityContext.runAsUser=0 redis bitnami/redis")

        if status != 0:
            raise("failed to install redis helm")

    def aws_token():
        status = os.system(f"echo \"@cym:registry=https://cym-dom-118330362824.d.codeartifact.us-east-1.amazonaws.com/npm/cym-repo/ \
        //cym-dom-118330362824.d.codeartifact.us-east-1.amazonaws.com/npm/cym-repo/:always-auth=true \
        //cym-dom-118330362824.d.codeartifact.us-east-1.amazonaws.com/npm/cym-repo/:_authToken=$(aws --region us-east-1 codeartifact get-authorization-token \
        --domain cym-dom --domain-owner 118330362824 --query authorizationToken --output text)\" > {dir}/Application/.secret/.npmrc")

        if status != 0:
            raise("failed to find to put the token")

    def mongodb_install():
        status = os.system("powershell -Command helm repo add bitnami https://charts.bitnami.com/bitnami; \
                             helm install --wait -n cymulate mongodb bitnami/mongodb --set auth.enabled=false;")
        if status != 0:
            raise("failed to install mongodb helm")

    def mongo_express_install():
        status = os.system("powershell -Command helm repo add cowboysysop https://cowboysysop.github.io/charts/; \
                             helm install -n cymulate mongo-express cowboysysop/mongo-express --set mongodbEnableAdmin=true;")
        if status != 0:
            raise("failed to install mongo-express helm")
    
    def mongo_dump():
        status = os.system(f"powershell -Command kubectl cp {dump_file_path} cymulate$(kubectl get pods -o name -n cymulate | grep -i mongodb | sed 's/pod//'):/tmp; \
                            kubectl exec -n cymulate -t $(kubectl get pods -o name -n cymulate | grep -i mongodb) -- mongorestore -d cymulate /tmp/cymulate; \
                            kubectl exec -n cymulate -t $(kubectl get pods -o name -n cymulate | grep -i mongodb) -- rm -rf /tmp/cymulate;")
        if status != 0:
            raise("failed to copy dump file")

    def verdaccio_install():
        status = os.system("powershell -Command helm repo add verdaccio https://charts.verdaccio.org; \
                            helm repo update; \
                            helm upgrade --install -f npm-values.yaml -n cymulate npm verdaccio/verdaccio;")
        if status != 0:
            raise("failed to install verdaccio")

    def run(cmd): 
        result = subprocess.run(cmd,stdout=subprocess.PIPE)
        return result.stdout.decode()

    if 'attack' and 'recon' and 'cymulate' not in run(['kubectl','get','ns']):
        create_namespace()
    

    if 'mongodb' not in run(['helm','-n','cymulate','list']):
        mongodb_install()
    
    if 'redis' not in run(['helm','-n','cymulate','list']):
        redis_install()

    if 'mongo-express' not in run(['helm','-n','cymulate','list']):
        mongo_express_install()
    
    mongo_dump()

    if 'npm' not in run(['helm','-n','cymulate','list']):
        verdaccio_install()

if __name__ == '__main__':
    # install_deps_windows()
    deploy_windows("","")



