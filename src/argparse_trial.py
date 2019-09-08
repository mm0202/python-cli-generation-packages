import requests
import json
import argparse


def bitflyer_getticker(product_code, is_json):
    end_point = "https://api.bitflyer.jp/v1/getticker"
    r = requests.get(end_point, params={'product_code': product_code})
    r_json = json.loads(r.text)
    if product_code == None:
        print('BTC_JPY')
    else:
        print(product_code)

    if is_json:
        print(r_json)
    else:
        print("bid:{}".format(r_json['best_bid']))
        print("ask{}".format(r_json['best_ask']))


parser = argparse.ArgumentParser(description='bitflyer api getticker')
parser.add_argument('-p', '--p', type=str, help=u'BTC_JPY or BTC_ETH')
parser.add_argument('-j', '--json', action='store_true', help=u"return json")

args = parser.parse_args()
bitflyer_getticker(product_code=args.p, is_json=args.json)
