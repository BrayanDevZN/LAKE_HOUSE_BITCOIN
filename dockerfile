FROM python:3.14.5

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "scr.CONTROLLER.main:app", "--host", "0.0.0.0", "--port", "8000"]