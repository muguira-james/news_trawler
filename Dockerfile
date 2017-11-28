FROM python:3
ADD ./ /app
WORKDIR /app
RUN pip install -r requirements.txt --find-links='./pips'
CMD [ "python", "trawler.py", "--configuration", "./config.conf" ]
