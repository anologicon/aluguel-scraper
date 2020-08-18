FROM python

WORKDIR /mydata
VOLUME [ "/mydata" ]


COPY scrapping.py ./
COPY VivaRealAirflow-6b7a6249dd4a.json ./

ENV GOOGLE_APPLICATION_CREDENTIALS=./VivaRealAirflow-6b7a6249dd4a.json

RUN pip install pandas
RUN pip install urllib3
RUN pip install beautifulsoup4
RUN pip install google-cloud
RUN pip install google-cloud-storage

CMD [ "python", "./scrapping.py"]