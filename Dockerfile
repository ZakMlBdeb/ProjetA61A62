FROM python:3.9.3-alpine

RUN pip install --upgrade pip

RUN adduser -D myuser
USER myuser
WORKDIR /home/myuser

COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

ENV PATH="/home/myuser/.local/bin:${PATH}"

COPY --chown=myuser:myuser . .

CMD ["python", "app.py", "runserver", "0.0.0.0:5000"]