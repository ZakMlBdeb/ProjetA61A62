FROM python:3.9

RUN pip install --upgrade pip

RUN adduser --disabled-login myuser
USER myuser
WORKDIR /home/myuser

COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

ENV PATH="/home/myuser/.local/bin:${PATH}"

COPY --chown=myuser:myuser . .

CMD ["python", "app.py"]
