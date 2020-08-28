FROM python

WORKDIR /mydata
VOLUME [ "/mydata" ]


COPY etl.py ./
COPY alugueis.csv ./

RUN pip install pandas

CMD [ "python", "./etl.py"]