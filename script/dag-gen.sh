cd dag-serverless

# Set the number of nodes in dag and your docker username
NUM_NODES=10
DOCKER_USERNAME=kevin1010607

# Generate the service, one service is corresponding to one node
cd service

# Build and push docker image
docker build -t $DOCKER_USERNAME/service .
docker push $DOCKER_USERNAME/service

# Generate the service and store its info to a json files.
# Also generate service yaml file in .service
python service_gen.py $NUM_NODES $DOCKER_USERNAME

# Deploy service to knative
for ((i=0; i<$NUM_NODES; i++)); do
  kubectl apply -f .service/service$i.yaml > /dev/null 2>&1
done
# Test service
for ((i=0; i<$NUM_NODES; i++)); do
  curl http://service$i.default.127.0.0.1.sslip.io:8080
done

# Generate the dag
cd ../dag
python dag_gen.py $NUM_NODES

# Delete dag info
rm -rf .dag

# Delete service and its info
cd ../service
for ((i=0; i<$NUM_NODES; i++)); do
  kubectl delete -f .service/service$i.yaml
done
rm -rf .service