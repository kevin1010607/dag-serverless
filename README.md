# dag-serverless

## Environment 

- Make sure you have installed `kind`, `kubectl`, `airflow`.
- Follow the step in [script/knative-setup.sh](script/knative-setup.sh) to set up knative cluster.
- Follow the step in [script/airflow-setup.sh](script/airflow-setup.sh) to set up airflow.
- [Optional] Follow the step in [script/knative-test.sh](script/knative-test.sh) to test knative service.

## Generate random dag and service

- Follow the step in [script/dag-gen.sh](script/dag-gen.sh) to generate the dag and service.

## Deploy the dag to your airflow

- Follow the step in [script/dag-deploy.sh](script/dag-deploy.sh) to deploy your dag.