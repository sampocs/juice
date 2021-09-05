FROM apache/airflow:2.1.2-python3.8

COPY --chown=airflow ./startup/* /usr/bin/ 

ENTRYPOINT [ "/bin/sh", "-c" ]