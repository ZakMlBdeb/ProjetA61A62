FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /app

COPY  . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]