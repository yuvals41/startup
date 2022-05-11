import os
from os.path import exists
import sys
import subprocess
import typer


def install_deps_windows():

    def wsl():
        status = os.system("wsl --install")

        if status != 0:
            raise("failed to install minikube")
    
    def enable_hyperv():
       status = os.system("powershell -Command if((Get-WindowsOptionalFeature -FeatureName Microsoft-Hyper-V-All -Online).State -ne 'Enabled') \
        { Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All}")
       if status != 0:
            raise("failed to enable hyperv")
    
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

    #checks if minikube exists
    if 'minikube' in os.getenv('Path'):
        minikube()

    #checks if aws exists
    if 'AWSCLIV2' in os.getenv('Path'):
        aws_cli()

    #checks if helm exists
    if exists(r'C:\ProgramData\chocolatey\bin\helm.exe'):
        helm("yes")
        
    #checks if skaffold exists
    if exists(r'C:\ProgramData\chocolatey\bin\skaffold.exe'):
        skaffold("yes")



    enable_hyperv()
    


def install_deps_linux():

    def minikube():
        status = os.system("cd /tmp && curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
        &&  install minikube-linux-amd64 /usr/local/bin/minikube")

        if status != 0:
            raise("failed to install minikube")

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
    #checks if minikube exists
    if not exists('/usr/local/bin/minikube'):
        minikube()
    #checks if kubectl exists
    if not exists('/usr/local/bin/kubectl') :
        kubectl()
    #checks if helm exists
    if not exists('/usr/local/bin/helm'):
        helm()
    #checks if skaffold exists
    if not exists('/usr/local/bin/skaffold'):
        skaffold()
    #checks if aws exists
    if not exists('/usr/local/bin/aws') :
        aws_cli()




def deploy_linux(dir, dump_file_path):

    def start_minikube():
        status = os.system("CHANGE_MINIKUBE_NONE_USER=true minikube start --driver=none")
        
        if status != 0:
            raise("failed to start minikube")

    def create_namespace():
        status = os.system(" kubectl create namespace attack; \
                             kubectl create namespace cymulate; \
                             kubectl create namespace recon")

        if status != 0:
            raise("failed to create namespace")

    def ingress_enable():
        status = os.system("minikube addons enable ingress \
                    &&  kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission")

        if status != 0:
            raise("failed to add ingresss or deleting ingress-nginx-admission")

    def redis_install():
        status = os.system(" helm repo add bitnami https://charts.bitnami.com/bitnami; \
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
        status = os.system(" helm repo add bitnami https://charts.bitnami.com/bitnami; \
                             helm install --wait -n cymulate mongodb bitnami/mongodb --set auth.enabled=false;")
        if status != 0:
            raise("failed to install mongodb helm")

    def mongo_express_install():
        status = os.system(" helm repo add cowboysysop https://cowboysysop.github.io/charts/; \
                             helm install -n cymulate mongo-express cowboysysop/mongo-express --set mongodbEnableAdmin=true;")
        if status != 0:
            raise("failed to install mongo-express helm")
    
    def mongo_dump():
        status = os.system(f"kubectl cp {dump_file_path} cymulate$(kubectl get pods -o name -n cymulate | grep -i mongodb | sed 's/pod//'):/tmp; \
                            kubectl exec -n cymulate -t $(kubectl get pods -o name -n cymulate | grep -i mongodb) -- mongorestore -d cymulate /tmp/cymulate; \
                            kubectl exec -n cymulate -t $(kubectl get pods -o name -n cymulate | grep -i mongodb) -- rm -rf /tmp/cymulate")
        if status != 0:
            raise("failed to copy dump file")
    def verdaccio_install():
        status = os.system("helm upgrade --install -f ~/npm-values.yaml -n cymulate npm verdaccio/verdaccio")
        if status != 0:
            raise("failed to copy dump file")

    def run(cmd): 
        result = subprocess.run(cmd,stdout=subprocess.PIPE)
        return result.stdout.decode()

    if 'Running' not in run(['minikube','status']):
        start_minikube()

    if 'attack' and 'recon' and 'cymulate' not in run(['kubectl','get','ns']):
        create_namespace()
    
    if "ingress-nginx" not in run(['kubectl', 'get', 'pods', '-n', 'ingress-nginx']):
        ingress_enable()

    if 'mongodb' not in run(['helm','-n','cymulate','list']):
        mongodb_install()
    
    if 'redis' not in run(['helm','-n','cymulate','list']):
        redis_install()

    if 'mongo-express' not in run(['helm','-n','cymulate','list']):
        mongo_express_install()
    
    mongo_dump()

    if 'npm' not in run(['helm','-n','cymulate','list']):
        verdaccio_install()

        
# app = typer.Typer()

# @app.command()
def main():
    if sys.platform == "linux":
        install_deps_linux()
        deploy_linux("~/Documents/cymulate/admin","~/Downloads/cymulate")


if __name__ == '__main__':
    main()
    
