cd dag-serverless

# Apply hello.yaml
kubectl apply -f env/hello.yaml

# Find url of hello service
kubectl get ksvc

# Request
curl http://$(kubectl get ksvc \
  --output=jsonpath="{.items[0].status.url}" \
  | sed -E 's/.+\///'):8080
# curl http://hello.default.127.0.0.1.sslip.io:8080

# Request with time
curl -s -w 'Total: %{time_total}s\n' \
  http://$(kubectl get ksvc \
  --output=jsonpath="{.items[0].status.url}" \
  | sed -E 's/.+\///'):8080
    
# Delete the service
kubectl delete -f env/hello.yaml