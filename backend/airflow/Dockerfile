FROM apache/airflow:2.1.2-python3.8

COPY --chown=airflow ./startup/* /usr/bin/ 

RUN pip install lxml

ENTRYPOINT [ "/bin/sh", "-c" ]