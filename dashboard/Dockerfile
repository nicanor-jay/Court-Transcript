FROM python:latest

WORKDIR dashboard

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY charts.py dashboard.py data_cache.py rds_utils.py utils.py ./

CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501"]