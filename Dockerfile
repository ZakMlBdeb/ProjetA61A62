FROM python:3.9

ENV VIRTUAL_ENV=/opt/env

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY  . .

CMD ["python", "app.py"]
