cd dag-serverless

# Create a kubernete cluster
kind create cluster --name knative --config env/knative-cluster-config.yaml

# Install knative-serving
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.10.2/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.10.2/serving-core.yaml

# Install kourier network layer
kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.10.0/kourier.yaml
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'
kubectl patch configmap/config-domain \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"127.0.0.1.sslip.io":""}}'

# Wait for kourier set up then Port forwarding
kubectl port-forward --namespace kourier-system \
  $(kubectl get pod -n kourier-system -l \
  "app=3scale-kourier-gateway" --output=jsonpath="{.items[0].metadata.name}") \
  8080:8080 19000:9000 8443:8443
  
# Delete cluster
kind delete cluster --name knative