FROM python:3.6

ENV PROJECT_ROOT /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install pip --upgrade
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker-utils/start.sh /start.sh

COPY . .

CMD ["/start.sh", "-docker"]
