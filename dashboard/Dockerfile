FROM python:3.12-slim

WORKDIR dashboard

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY charts.py Home_Page.py data_cache.py rds_utils.py utils.py ./
COPY pages ./pages
COPY images ./images
COPY .streamlit ./.streamlit 

CMD ["streamlit", "run", "Home_Page.py", "--server.port", "8501"]