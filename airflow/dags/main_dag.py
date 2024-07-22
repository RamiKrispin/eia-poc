from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

import os

default_args = {
    "owner" : "Rami"
}


EIA_API_KEY = os.getenv('EIA_API_KEY')



with DAG(
    dag_id = "eia_refresh",
    description = "EIA data and forecast pipeline",
    default_args =  default_args,
    start_date= days_ago(1),
    schedule_interval = "@daily",
    tags = ["test", "bash", "python"],
    template_searchpath = "/airflow/scripts/"
) as dag:

    taskA = DockerOperator(
        task_id = "task_A",
        image = "docker.io/rkrispin/forecast-poc:0.0.0.9011",
        command = "bash /scripts/data_refresh/eia_data_refresh_airflow.sh ",
        # command = "ls /scripts/data_refresh/",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        api_version="auto",
        xcom_all= True,
        cpus = 1,
        mount_tmp_dir= False,
        environment={"EIA_API_KEY": os.getenv("EIA_API_KEY")},
        mounts= [
            Mount(source = "/Users/ramikrispin/Personal/poc/eia-poc/", target = "/scripts", type = "bind")
        ]
    )

taskA