FROM python:3.8
RUN pip install --upgrade pip
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python" ]
CMD ["app.py"]