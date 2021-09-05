#!/bin/bash

if [[ -f "/opt/airflow/database/airflow.db" ]];
then
    echo "Database already initialized."
else
    echo "Initializing DB..."
    airflow db init 
fi

# Create a main user if it hasn't been done already
if [[ "$(airflow users list | grep ${AIRFLOW_USERNAME} | wc -l)" == "0" ]]; then
    echo "Creating user..."
    airflow users create \
        -u ${AIRFLOW_USERNAME} \
        -e ${AIRFLOW_EMAIL} \
        -f ${AIRFLOW_FIRSTNAME} \
        -l ${AIRFLOW_LASTNAME} \
        -p ${AIRFLOW_PASSWORD} \
        -r Admin
else
    echo "User: ${AIRFLOW_USERNAME} already exists."
fi

if [[ "$(airflow connections get juice-postgres)" == "" ]]; then 
    echo "Creating juice-db connection..."
    airflow connections add "juice-postgres" \
        --conn-uri "postgresql://${JUICE_DB_USER}:${JUICE_DB_PASSWORD}@db:5432/${JUICE_DB_NAME}"
else
    echo "juice-postgres connection already exists."
fi

echo "Starting scheduler..."
airflow scheduler 