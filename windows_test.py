import os
from os.path import exists
import sys
import subprocess
import typer


def install_deps_windows():

    # def minikube():
        # status = os.system("cd /tmp && curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
        # &&  install minikube-linux-amd64 /usr/local/bin/minikube")

        # if status != 0:
        #     raise("failed to install minikube")

    def wsl():
        status = os.system("wsl --install")

        if status != 0:
            raise("failed to install wsl")

    def install_docker_desktop():

        status = os.system("Install-Module -Name DockerMsftProvider -Repository PSGallery -Force")

        if status != 0:
            raise("failed to install docker")

    def kubectl():
        status = os.system("cd /tmp && curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl \
        &&  install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl")

        if status != 0:
            raise("failed to install kubectl")
    def helm():   
        status = os.system("curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash")
            
        if status != 0:
            raise("failed to install helm")
    
    def skaffold():
        status = os.system("cd /tmp && curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 \
        &&  install skaffold /usr/local/bin/")

        if status != 0:
            raise("failed to install skaffold")
    
    def aws_cli():
        status = os.system("curl -fqsSL \"https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip\" -o \"/tmp/awscliv2.zip\" \
        && unzip -q -o /tmp/awscliv2.zip -d /tmp && /tmp/aws/install -b /usr/local/bin \
        && chmod +x /usr/local/bin/aws \
        && rm -rf /tmp/aws /tmp/awscliv2.zip")

        if status != 0:
            raise("failed to install aws cli")
    
    # wsl()
    install_docker_desktop()
    # #checks if minikube exists
    # if not exists('/usr/local/bin/minikube'):
    #     minikube()
    # #checks if kubectl exists
    # if not exists('/usr/local/bin/kubectl') :
    #     kubectl()
    # #checks if helm exists
    # if not exists('/usr/local/bin/helm'):
    #     helm()
    # #checks if skaffold exists
    # if not exists('/usr/local/bin/skaffold'):
    #     skaffold()
    # #checks if aws exists
    # if not exists('/usr/local/bin/aws') :
    #     aws_cli()




def main():
    # if sys.platform == "linux":
    #     install_deps_linux()
    #     deploy_linux("~/Documents/cymulate/admin","~/Downloads/cymulate")
    # if sys.platform == "windows":
        install_deps_windows()


if __name__ == '__main__':
    main()
    
