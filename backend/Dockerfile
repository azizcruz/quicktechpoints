FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY . /backend
COPY .env /backend/src/src/.env
COPY backend/requirements.txt /backend/requirements.txt
RUN pip install -r /backend/requirements.txt
RUN pip install psycopg2-binary
RUN python backend/src/manage.py collectstatic --no-input
RUN chmod 755 backend/src/static

