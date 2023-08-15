cd dag-serverless

# Make sure you export AIRFLOW_HOME
echo $AIRFLOW_HOME

# Check the dag file
DAG_FILENAME=$PWD/dag/.dag/dag.json
if [ -e $DAG_FILENAME ]; then
    echo "Dag file exists."
else
    echo "Dag file does not exist."
    exit 0
fi

# Copy a dag info file to airflow
cp $DAG_FILENAME $AIRFLOW_HOME/dags

# Copy dag python file to airflow and replace the path of dag info file
cp dag.py $AIRFLOW_HOME/dags
sed -i "" "s#<DAG_FILENAME>#$AIRFLOW_HOME/dags/dag.json#g" $AIRFLOW_HOME/dags/dag.py