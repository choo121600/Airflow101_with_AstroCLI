from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# DAG 정의
default_args = {
    'owner': 'user',
    'start_date': datetime(2023, 10, 1),
}

# DAG 인스턴스 생성
dag = DAG('example_simple_dag2', default_args=default_args, schedule_interval='@daily')

# 태스크 정의
def start_task():
    print("DAG가 시작되었습니다.")

def task_1():
    print("Task 1이 실행되었습니다.")

def task_2():
    print("Task 2가 실행되었습니다.")

def end_task():
    print("DAG가 종료되었습니다.")

# PythonOperator를 사용하여 태스크 생성
start = PythonOperator(
    task_id='start_task',
    python_callable=start_task,
    dag=dag,
)

t1 = PythonOperator(
    task_id='task_1',
    python_callable=task_1,
    dag=dag,
)

t2 = PythonOperator(
    task_id='task_2',
    python_callable=task_2,
    dag=dag,
)

end = PythonOperator(
    task_id='end_task',
    python_callable=end_task,
    dag=dag,
)

# 태스크 간의 의존성 설정
start >> t1 >> t2 >> end
