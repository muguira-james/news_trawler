FROM python:2.7
ADD ./ /app
WORKDIR /app
RUN pip install --no-index --find-links=./pips -r requirements.txt
CMD ['python', 'trawler.py']
