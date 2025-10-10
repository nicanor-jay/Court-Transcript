FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY create_email.py send_email.py verify_email.py aws_utils.py ./

CMD [ "send_email.handler"]