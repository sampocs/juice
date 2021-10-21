FROM apache/airflow:2.1.2-python3.9

COPY --chown=airflow ./airflow/startup/* /usr/bin/ 
COPY --chown=airflow requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "/bin/sh", "-c" ]