import requests
import json
import click


@click.group()
def cli():
    pass


@click.command()
@click.option('--product_code', '-p', default='BTC_JPY', help=u'BTC_JPY or BTC_ETH')
@click.option('--is_json/--no-is_json', default=False, help=u"return json")
def bitflyer_getticker(product_code='BTC_JPY', is_json=False):
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


cli.add_command(bitflyer_getticker)

if __name__ == "__main__":
    cli()
