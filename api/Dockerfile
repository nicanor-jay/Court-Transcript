FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY api_utils.py .
COPY api.py .
COPY index.html .

CMD python3 api.py