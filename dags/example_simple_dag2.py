from airflow.decorators import dag, task
from datetime import datetime

# DAG 정의
default_args = {
    'owner': 'user',
    'start_date': datetime(2023, 10, 1),
}

@dag(schedule_interval='@daily', default_args=default_args)
def example_simple_dag():
    @task
    def start_task():
        print("DAG가 시작되었습니다.")

    @task
    def task_1():
        print("Task 1이 실행되었습니다.")

    @task
    def task_2():
        print("Task 2가 실행되었습니다.")

    @task
    def end_task():
        print("DAG가 종료되었습니다.")

    start = start_task()
    t1 = task_1()
    t2 = task_2()
    end = end_task()

    start >> t1 >> t2 >> end

dag_instance = example_simple_dag()
