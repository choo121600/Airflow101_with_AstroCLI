# 개요

2024년 10월 26일 토요일, 부산에서 열린 "Python PIP 배포 실습 및 Airflow 101 with Astro CLI Hands-on" 세미나 중의 "Airflow 101 with Astro CLI"의 자료입니다.

# 발표자료
[발표자료 보기](https://docs.google.com/presentation/d/1XXIk5Gv_Tut427IKsBzjIUPpkNp64jseWK1lc3uK3Lg/edit?usp=sharing)

# 자료 내용
Airflow 101 with Astro CLI  
Hands-on: 데일리 뉴스 요약 및 투자 조언 메시징 서비스 구축하기

# 준비물
- Python 3.10 이상
- Docker Desktop
- Astro CLI
- code editor

# 핸즈온 순서
- 프로젝트 Clone
- Astro CLI를 활용하여 Airflow 실행과 중지, 재시작
- DAG를 작성하는 두 가지 방법
- 실패, 성공시 알림을 보내는 DAG 만들기
    - 준비물: Google 2단계 인증 만들기, Slack API 적용
    - DAG 작성
- 프로젝트 시작
    - 준비물: Chat GPT Key 받아오기
    - DAG 작성

# DAG 예시 소스코드
- dags
    - example_simple_dag.py : 간단한 DAG 를 만드는 방법 1 예제
    - example_simple_dag2.py : 간단한 DAG 를 만드는 방법 2 예제
    - notification_example_dag.py : Slack과 Email로 알림을 보내는 DAG 예제
    - project_dag.py : 뉴스 요약 및 투자 조언 메시징 서비스 구축 DAG


# 실행 방법
1. Astro CLI 설치
    - [Astro CLI 설치 가이드](https://www.astronomer.io/docs/astro/cli/install-cli)
2. Astro CLI로 Airflow 실행
    - `astro dev start`
3. [http://localhost:8080](http://localhost:8080) 접속
4. .env 파일, airflow_settings.yaml 파일 작성
5. DAG 활성화
6. DAG 실행

# 주요 Astro CLI 명령어
- `astro dev --help` : 도움말
- `astro dev init` : Airflow 초기화
- `astro dev start` : Airflow 실행
- `astro dev stop` : Airflow 중지
- `astro dev restart` : Airflow 재시작
- `astro dev kill` : Airflow 강제 중지



# .env 작성
```
# .env
OPENAI_API_KEY="sk-xxxxxx"

AIRFLOW__SMTP__SMTP_HOST="smtp.gmail.com"
AIRFLOW__SMTP__SMTP_PORT="587"
AIRFLOW__SMTP__SMTP_SSL="False"
AIRFLOW__SMTP__SMTP_USER="your-email"
AIRFLOW__SMTP__SMTP_STARTTLS="True"
AIRFLOW__SMTP__SMTP_MAIL_FROM="your-email"
AIRFLOW__SMTP__SMTP_PASSWORD="google-2nd-password"
```

# airflow_settings.yaml 작성
```
# airflow_settings.yaml
airflow:
  connections:
    - conn_id: slack_connection_id
      conn_type: HTTP
      conn_host:
      conn_schema:
      conn_login:
      conn_password: slack_webhook_url
      conn_port:
      conn_extra:
  pools:
    - pool_name:
      pool_slot:
      pool_description:
  variables:
    - variable_name:
      variable_value:
  configurations:
    - section:
    - key:
    - value:

```

# 질문 및 문의
- Airflow 한국사용자모임 포럼: [https://discourse.airflow-kr.org/](https://discourse.airflow-kr.org/)
- Airflow 한국사용자모임 오픈카톡: [https://open.kakao.com/o/gM4hR8Pg](https://open.kakao.com/o/gM4hR8Pg)
