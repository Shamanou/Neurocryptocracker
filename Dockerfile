FROM gw000/keras-full
RUN pip install tgym
RUN apt-get update && apt-get install -y python-tk curl gzip
WORKDIR /
COPY src/ /src/
COPY generators/ /generators/
COPY trader/ /trader/
COPY train.sh /train.sh
COPY trade.sh trade.sh
RUN chmod +x /src/train.py
RUN chmod +x /train.sh
RUN chmod +x /trade.sh
RUN chmod +x /trader/main.py
WORKDIR src/data
RUN curl http://api.bitcoincharts.com/v1/csv/cexEUR.csv.gz | gunzip -| cut -d, -f2,3  > EUR-history.csv
RUN curl http://api.bitcoincharts.com/v1/csv/cexUSD.csv.gz | gunzip - | cut -d, -f2,3 > USD-history.csv
RUN curl http://api.bitcoincharts.com/v1/csv/cexRUB.csv.gz | gunzip - | cut -d, -f2,3 > RUB-history.csv
WORKDIR /
RUN ./train.sh
RUN cp /src/model.*.json /trader/
RUN cp /src/model.*.h5 /trader/
CMD ./trade.sh
