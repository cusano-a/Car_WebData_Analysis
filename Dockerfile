# app/Dockerfile

FROM python:3.10-slim

WORKDIR app/Serving

# Setup
COPY ./Serving/requirements_serving.txt /app/Serving
RUN pip3 install -r requirements_serving.txt

COPY ./Serving /app/Serving
COPY ./Modeling/models/XGB_final.joblib /app/Modeling/models/XGB_final.joblib

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
