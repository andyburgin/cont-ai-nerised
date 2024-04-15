# K8s GPT
Instructions for setup of K8sGPT in Kind, using Kind and OpenAI ChatGPT, download stable code model from https://huggingface.co/TheBloke/stable-code-3b-GGUF

## Setup Cluster
```
kind create cluster --config 01-kind/kind-cluster.yaml

kubectl get nodes

kubectl get pods -A
```

## Config OpenAI

```
k8sgpt auth add openai
<enter openai key>

k8sgpt auth list
```
This stores your openAI key in ~/.config/k8sgpt/k8sgpt.yaml (on linux, see docs for other OS locations).

## Deploy Bad Nginx
```
kubectl create ns demo

kubectl apply -f 02-nginx-deploy/nginx-bad.yaml -n demo

kubectl get pods -n demo -w
```

## What's Up ?
```
k8sgpt analyse

k8sgpt analyse --explain

k8sgpt analyse --explain --with-doc

k8sgpt analyze --explain --filter=Pod --namespace=demo

k8sgpt analyse --explain --interactive
```
Tip - if you don't want to send your private stuff to openai use `--anonymize` - not all resource kinds are anonymised, see docs for which ones.


## Filters and Integrations

Filters are the analysers that identify problems 
```
k8sgpt filters list
```
Only show ones that are applicable, netpols would show if CNI supported it.

Full list - https://github.com/k8sgpt-ai/k8sgpt/tree/main/pkg/analyzer

Can filter on filters in the analyser 
```
k8sgpt analyse --filter=VulnerabilityReport --explain
```
Integrations are hooks into other running applications
```
 k8sgpt integration list
 #k8sgpt integration activate trivy
 #k8sgpt integration activate prometheus
```
Note activating the `trivy` integration will install it onto the cluster, `prometheus` installs the ability to analyse prom config.

# Install the Operator

## Install Prometheus and Grafana Prerequisites
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create ns monitoring
helm install prom prometheus-community/kube-prometheus-stack -n monitoring --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
kubectl get pods -n monitoring -w
```

## Create Namespace
```
kubectl create ns k8sgpt-operator 
```

## Create OpenAI Secret
```
export OPENAI_TOKEN=<YOUR API KEY HERE>
kubectl create secret generic k8sgpt-secret --from-literal=openai-api-key=$OPENAI_TOKEN -n k8sgpt-operator
```

## Install Operator
```
helm repo add k8sgpt https://charts.k8sgpt.ai/
helm repo update
helm install release k8sgpt/k8sgpt-operator -n k8sgpt-operator --set serviceMonitor.enabled=true --set grafanaDashboard.enabled=true
kubectl get pods -n k8sgpt-operator -w
```

## Create instance
```
kubectl apply -f 03-k8sgpt-operator/k8sgpt-deploy.yaml
kubectl get pods -n k8sgpt-operator -w
```

## Wait for Results
```
kubectl get results -n k8sgpt-operator
kubectl get result demonginxdeploymentxxxxxxxxxx -n k8sgpt-operator -o json
```
Note `error` is from the filter/analyser. The `details` is the results of the analysis from openAI backend, 

## To the Dashboards
```
kubectl get service -n monitoring

kubectl port-forward service/prom-kube-prometheus-stack-prometheus -n monitoring 9090:9090
```
#Point a browser at http://localhost:9090/ and check `k8sgpt_number_of_results` and `k8sgpt_number_of_results_by_type`

```
kubectl port-forward service/prom-grafana -n monitoring 3000:80
http://localhost:3000/
```

Creds `admin/prom-operator` see "K8sGPT Overview Dashboard"


# Install Local-AI

## Install Helm Chart
```
helm repo add go-skynet https://go-skynet.github.io/helm-charts/
kubectl create ns local-ai
helm install local-ai go-skynet/local-ai -f 04-local-ai/values.yaml -n local-ai
kubectl get pods -n local-ai -w
```

## Install Model(s)
Auto download fails due to url validation checks, so this is a workaround, models can be loaded from internet, or in this case from local models folder on workstation.
```
cd models
sudo python -m http.server 80

kubectl exec -ti  local-ai-xxxxxxxxx-xxxxx -n local-ai bash
cd /models
curl http://192.168.xx.xx/stable-code-3b-q4_k_m.gguf -o stable-code-3b-q4_k_m.gguf
```

## Local Analysis Using in Cluster Local-ai
```
kubectl port-forward svc/local-ai 8080:80 -n local-ai
k8sgpt auth add --backend localai --model stable-code-3b-q4_k_m.gguf --baseurl http://localhost:8080/v1
k8sgpt auth list
k8sgpt analyze --explain --backend localai
```

# Replace the k8sgpt instance

```
kubectl delete -f 03-k8sgpt-operator/k8sgpt-deploy.yaml
kubectl delete result -n k8sgpt-operator -l k8sgpts.k8sgpt.ai/backend=openai 

kubectl -n local-ai apply -f 04-local-ai/k8sgpt-deploy.yaml
kubectl get pods -n local-ai -w
```

## Wait for Results
```
kubectl get results -n local-ai
kubectl describe result demonginxdeploymentxxxxxxxxxxxxxx -n local-ai
```

# Tidy up
```
kubectl delete -f 04-local-ai/k8sgpt-deploy.yaml
kubectl delete result -l k8sgpts.k8sgpt.ai/backend=localai -n local-ai

kind delete cluster
```