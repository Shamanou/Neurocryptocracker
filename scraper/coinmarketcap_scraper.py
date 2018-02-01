import time

import pandas

base = "https://coinmarketcap.com"

coin_page = pandas.read_html(base + "/coins")[0][0:25]
coins = coin_page[['Name']].values.tolist()
coins = [''.join(x[0].strip().split(' ')[1:]) for x in coins]
for name in coins:
    print 'collecting data for ' + name
    try:
        bitcoin_market_info = pandas.read_html(
            base + "/currencies/" + name.lower() + "/historical-data/?start=20130428&end=" + time.strftime(
                "%Y%m%d"))[0]
        bitcoin_market_info.to_csv(name + ".csv")
    except:
        print name + " couldnt be collected"
