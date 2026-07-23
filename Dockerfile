FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY examples/ ./examples/
EXPOSE 5000
CMD ["python", "src/app.py"]