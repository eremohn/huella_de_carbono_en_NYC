FROM python:3.10
COPY ./code /usr/app/
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install cron
RUN crontab -l | { cat; echo "0 12 7 * * /usr/local/bin/python /usr/app/ml-yellow.py"; } | crontab -
RUN crontab -l | { cat; echo "0 15 7 * * /usr/local/bin/python /usr/app/ml-green.py"; } | crontab -
RUN crontab -l | { cat; echo "0 18 7 * * /usr/local/bin/python /usr/app/ml-co2.py"; } | crontab -
CMD ["cron", "-f"]