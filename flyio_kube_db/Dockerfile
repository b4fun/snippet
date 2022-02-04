FROM python:3.9

RUN mkdir -p /app
ADD app.py /app/app.py
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

CMD python /app/app.py