FROM python

WORKDIR /mydata
VOLUME [ "/mydata" ]


COPY scrapping.py ./
COPY aluguel-data-project-63b6ff0f324c.json ./

ENV GOOGLE_APPLICATION_CREDENTIALS=./aluguel-data-project-63b6ff0f324c.json

RUN pip install pandas
RUN pip install urllib3
RUN pip install beautifulsoup4
RUN pip install google-cloud
RUN pip install google-cloud-storage
RUN pip install python-slugify

CMD [ "python", "./scrapping.py"]