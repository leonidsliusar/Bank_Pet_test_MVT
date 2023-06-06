FROM python:3.10.6-slim

WORKDIR /bank
ENV PYTHONWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY . .

RUN pip install --upgrade pip
ADD requirements.txt /bank/requirements.txt
RUN pip install -r requirements.txt

ADD ../.. /bank/
EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000