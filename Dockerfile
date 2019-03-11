FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs

COPY . code
WORKDIR code

RUN npm --prefix webapp install
RUN npm --prefix webapp install @vue/cli@latest
RUN npm run --prefix webapp build

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:$PORT --access-logfile - phonebook.wsgi:application