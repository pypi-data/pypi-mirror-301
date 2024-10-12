FROM python:3.7.6-slim-buster

# enforce stdout to be in correct order
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /dlds-aws-scheduler
WORKDIR /dlds-aws-scheduler

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH /dlds-aws-scheduler

COPY ./dldsaws dldsaws

ENTRYPOINT ["python", "dldsaws/dlds_aws_scheduler.py", "--config", "/etc/dldsaws/config.yml"]
