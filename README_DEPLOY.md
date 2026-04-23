# AI Career Agent - Azure Deployment Guide

## Prerequisites

Before starting, ensure you have:

1. **Azure CLI** - [Install Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
   ```bash
   az login
   az account set --subscription YOUR_SUBSCRIPTION_ID
   ```

2. **Docker** - [Install Docker](https://docs.docker.com/get-docker/)
   ```bash
   docker --version
   ```

3. **kubectl** - [Install kubectl](https://kubernetes.io/docs/tasks/tools/)
   ```bash
   kubectl version --client
   ```

4. **Jenkins** with:
   - Azure Credentials Plugin
   - Docker Pipeline Plugin
   - Azure Service Principal credentials configured

---

## Step 1: Run Azure Setup Script

Execute the provisioning script to create all Azure resources:

```bash
chmod +x azure-setup.sh
./azure-setup.sh
```

This creates:
- Resource Group: `career-agent-rg`
- Container Registry: `devopsmlops.azurecr.io`
- AKS Cluster: `career-agent-aks` (2 nodes)
- Kubernetes Namespace: `career-agent`
- Secrets: `career-agent-secrets`

---

## Step 2: Get ACR Credentials

Retrieve the ACR admin credentials for Jenkins:

```bash
az acr credential show --name devopsmlops
```

You will get:
- **Username**: `devopsmlops`
- **Password 1**: `<password>`
- **Password 2**: `<password>`

Use these in Jenkins as the `acr-credentials` Username/Password credential.

---

## Step 3: Create Service Principal

Create a service principal with contributor access to your resource group:

```bash
az ad sp create-for-rbac \
    --name jenkins-career-agent \
    --role Contributor \
    --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/career-agent-rg
```

Output:
```json
{
  "appId": "xxxx-xxxx-xxxx",
  "password": "xxxx-xxxx-xxxx",
  "tenant": "xxxx-xxxx-xxxx"
}
```

Use these values in Jenkins as the `azure-sp` Azure Service Principal credential:
- **Client ID**: `appId`
- **Client Secret**: `password`
- **Tenant ID**: `tenant`
- **Subscription ID**: From `az account show`

---

## Step 4: Add Credentials in Jenkins

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Add **Username/Password** credential (ID: `acr-credentials`):
   - Username: `devopsmlops`
   - Password: `<from Step 2>`
3. Add **Azure Service Principal** credential (ID: `azure-sp`):
   - Client ID, Client Secret, Tenant ID, Subscription ID

---

## Step 5: Create Jenkins Pipeline

1. Create a new **Pipeline** job in Jenkins
2. Point to this repository's `Jenkinsfile`
3. Run the build

---

## Kubernetes Resources

The `k8s/` directory contains:

| File | Description |
|------|-------------|
| `namespace.yaml` | Creates `career-agent` namespace |
| `deployment.yaml` | 2 replicas, 256Mi RAM, port 5000 |
| `service.yaml` | LoadBalancer on port 80 |

---

## Troubleshooting

### Pod CrashLoopBackOff

Check pod logs:
```bash
kubectl get pods -n career-agent
kubectl logs <pod-name> -n career-agent
kubectl describe pod <pod-name> -n career-agent
```

Common causes:
- Missing environment variables → Verify secrets exist
- Application error → Check logs for Python exceptions
- Resource limits → Increase memory/CPU in deployment.yaml

### Image Pull Errors

Verify ACR is attached to AKS:
```bash
az aks show --resource-group career-agent-rg --name career-agent-aks --query servicePrincipalProfile
az acr show --name devopsmlops --query id
```

If not attached:
```bash
az aks update --resource-group career-agent-rg --name career-agent-aks --attach-acr devopsmlops
```

### Missing Secrets

Recreate the secret:
```bash
kubectl create secret generic career-agent-secrets \
    --namespace career-agent \
    --from-literal=groq-api-key=your_groq_key \
    --from-literal=tavily-api-key=your_tavily_key
```

### Verify Deployment

```bash
kubectl get all -n career-agent
kubectl get svc -n career-agent
kubectl rollout status deployment/career-agent -n career-agent
```

Get external IP:
```bash
kubectl get svc -n career-agent -w
```