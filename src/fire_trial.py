import requests
import json
import fire


class Bitflyer():
    def __init__(self, end_point="https://api.bitflyer.jp/v1/getticker"):
        self.end_point = end_point

    def getticker(self, product_code='BTC_JPY', is_json=False):
        r = requests.get(self.end_point, params={'product_code': product_code})
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


if __name__ == "__main__":
    fire.Fire(Bitflyer)
