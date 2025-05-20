FROM python:slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY gcp_function_brute.py /app/gcp_function_brute.py
ENTRYPOINT ["python", "/app/gcp_function_brute.py"]

