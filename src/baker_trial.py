import requests
import json
import baker


@baker.command(params={"product_code": "'BTC_JPY or BTC_ETH", "is_json": "return json"})
def bitflyer_getticker(product_code='BTC_JPY', is_json=False):
    """bitflyer api getticker                                                                  
    """
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


baker.run()
