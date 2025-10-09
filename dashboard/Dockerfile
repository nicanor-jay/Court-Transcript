FROM python:3.12-slim

WORKDIR dashboard

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY charts.py dashboard.py data_cache.py rds_utils.py utils.py /pages ./

CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501"]