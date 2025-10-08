FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}

COPY email/requirements.txt .

RUN pip3 install -r requirements.txt

COPY email/create_email.py email/rds_utils.py ./

CMD [ "create_email.handler"]