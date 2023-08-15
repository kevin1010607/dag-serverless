# Set AIRFLOW_HOME, add it to ~/.bashrc
export AIRFLOW_HOME=$HOME/airflow

# Initailize airflow db
cd $HOME
mkdir -p airflow
mkdir -p airflow/dags
airflow db reset
airflow db init

# Modify airflow config file
cd airflow
# MacOS
sed -i '' 's#load_examples.*#load_examples = False#g' airflow.cfg
# Linux
# sed -i 's#load_examples.*#load_examples = False#g' airflow.cfg

# Create a user
airflow users create \
  --username admin \
  --firstname FIRST_NAME \
  --lastname LAST_NAME \
  --role Admin \
  --email admin@example.org

# Use another terminal
airflow webserver -p 8081

# Use another terminal
airflow scheduler