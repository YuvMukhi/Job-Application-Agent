#!/bin/bash

set -e

ACR_NAME="devopsmlops"
RESOURCE_GROUP="career-agent-rg"
LOCATION="eastus"
AKS_CLUSTER="career-agent-aks"

echo "=== Azure Setup for AI Career Agent ==="
echo "ACR Name: $ACR_NAME"
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"
echo ""

echo "Step 1: Creating Resource Group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo ""
echo "Step 2: Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

echo ""
echo "Step 3: Enabling ACR Admin User..."
az acr update --name $ACR_NAME --admin-enabled true

echo ""
echo "Step 4: Creating AKS Cluster..."
az aks create \
    --resource-group $RESOURCE_GROUP \
    --name $AKS_CLUSTER \
    --node-count 2 \
    --generate-ssh-keys \
    --attach-acr $ACR_NAME

echo ""
echo "Step 5: Getting AKS Credentials..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --overwrite-existing

echo ""
echo "Step 6: Creating Kubernetes Secrets..."
kubectl create secret generic career-agent-secrets \
    --namespace career-agent \
    --from-literal=groq-api-key=YOUR_GROQ_API_KEY_HERE \
    --from-literal=tavily-api-key=YOUR_TAVILY_API_KEY_HERE

echo ""
echo "Step 7: Creating Namespace..."
kubectl create namespace career-agent

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Get ACR credentials (for Jenkins 'acr-credentials'):"
echo "   az acr credential show --name $ACR_NAME"
echo ""
echo "2. Create Service Principal for AKS (for Jenkins 'azure-sp'):"
echo "   az ad sp create-for-rbac --name jenkins-career-agent --role Contributor --scopes /subscriptions/\$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP"
echo ""
echo "3. Update the secret with real API keys:"
echo "   kubectl delete secret career-agent-secrets -n career-agent"
echo "   kubectl create secret generic career-agent-secrets \\"
echo "       --namespace career-agent \\"
echo "       --from-literal=groq-api-key=your_actual_groq_key \\"
echo "       --from-literal=tavily-api-key=your_actual_tavily_key"