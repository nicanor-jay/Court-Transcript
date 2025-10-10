FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}

COPY email/requirements.txt .

RUN pip3 install -r requirements.txt

COPY email/create_email.py email/send_email.py email/verify_email.py email/aws_utils.py ./

CMD [ "send_email.handler"]