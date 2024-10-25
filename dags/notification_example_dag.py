from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.decorators import dag, task
from datetime import datetime
import os

FROM_EMAIL = os.getenv('AIRFLOW__SMTP__SMTP_MAIL_FROM')


# Slack 및 이메일 알림 포멧설정 및 전송 Operator
def notification(context):
    slack_icon = "large_green_circle" if context.get('task_instance').state == "success" else "red_circle"
    task_state = context.get('task_instance').state
    task_id = context.get('task_instance').task_id
    dag_id = context.get('task_instance').dag_id
    task_exec_date = context.get('execution_date')
    task_log_url = context.get('task_instance').log_url

    slack_msg = f"""
        Task {task_state} :{slack_icon}:
        *Dag*: {dag_id} 
        *Task*: {task_id}  
        *Execution Time*: {task_exec_date}  
        *Log Url*: {task_log_url} 
    """

    html_msg = f"""
    <html>
      <body>
        <h2>Task Notification</h2>
        <p>
          <strong>Task State:</strong> {task_state}<br>
          <strong>DAG:</strong> {dag_id}<br>
          <strong>Task:</strong> {task_id}<br>
          <strong>Execution Time:</strong> {task_exec_date}<br>
          <strong>Log URL:</strong> <a href="{task_log_url}">{task_log_url}</a><br>
        </p>
      </body>
    </html>
    """

    slack_webhook_task = SlackWebhookOperator(
        task_id='slack_notification',
        slack_webhook_conn_id='slack_connection_id',
        message=slack_msg,
        channel='#test'
    )
    slack_webhook_task.execute(context=context)

    email_task = EmailOperator(
        task_id='email_notification',
        to={FROM_EMAIL},
        subject=f'Task Notification{dag_id}',
        html_content=html_msg
    )
    email_task.execute(context=context)


# 기본 인자 설정
default_args = {
    "owner": "airflow",
    "retries": 0,
    # 만약 실패 또는 성공시 커스텀 알림을 받고 싶다면 아래 주석을 해제하고 notification 함수를 추가하세요
    # "on_failure_callback": notification,
    # "on_success_callback": notification,
    "email": [FROM_EMAIL],
    # 만약 실패 또는 재시도시 기본 알림을 이메일로 받고 싶다면 아래 주석을 해제하세요
    # "email_on_failure": True,
    # "email_on_retry": True
}

@dag(
    start_date=datetime(2024, 10, 25),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    tags=["example"]
)
def slack_and_email_notifications():

    # 실패를 발생시키는 함수
    @task
    def fail():
        raise Exception("Task failed intentionally for testing purpose")

    # 성공을 알리는 함수
    @task
    def success():
        print("success")

    # Task dependencies 설정
    fail() >> success()


slack_and_email_notifications()
