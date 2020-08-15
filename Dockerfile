FROM python

WORKDIR /mydata
VOLUME [ "/mydata" ]

COPY scrapping.py ./

RUN pip install pandas
RUN pip install urllib3
RUN pip install beautifulsoup4

CMD [ "python", "./scrapping.py"]