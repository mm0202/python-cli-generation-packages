以下の記事を参考にbaker, click, fireを比較。
ざっくり見ただけなので、間違ってるところがあったら、指摘していただけるとありがたいです。

[コマンドラインツールを自動生成できるPython Fireと他のライブラリ比べてみた](https://paiza.hatenablog.com/entry/2017/03/10/%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%83%A9%E3%82%A4%E3%83%B3%E3%83%84%E3%83%BC%E3%83%AB%E3%82%92%E8%87%AA%E5%8B%95%E7%94%9F%E6%88%90%E3%81%A7%E3%81%8D%E3%82%8BPython_Fire%E3%81%A8%E4%BB%96%E3%81%AE)

# 比較に利用する、コマンド定義コード
※ ほぼほぼ、上述リンクのコピペ。一部、比較用に調整。
## baker
```python
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
```
シンプルで、設定が簡単そう。引数がそのままオプションになるみたいなので、短いオプションにしたい場合は、`product_code=p`みたいな感じで関数内で置き換えが必要になりそう。

## click
```python
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
```
ネスティングコマンドが試したかったので、参考にした記事から少し調整。細かい設定が可能そうで、短縮版のオプションの定義も簡単そう。

## fire
```python
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
```
簡単実装。fireパッケージをimportして、最後に`fire.Fire()`とするだけでOK。クラスにも対応。クラスの場合は`fire.Fire(クラス名)`で実装。機能も豊富そうだけど、オプションの解説を設定できなさそうなのが難点。

# ヘルプ比較
## baker
```shell
$ python baker_trial.py --help
Usage: baker_trial.py COMMAND <options>

Available commands:
 bitflyer_getticker  bitflyer api getticker

Use 'baker_trial.py <command> --help' for individual command help.
```
短くシンプルで見やすい。

## click
```shell
$ python click_trial.py --help
Usage: click_trial.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  bitflyer-getticker
```
baker同様、短くシンプルで見やすい。

## fire
```shell
# ヘルプオプションあり
$ python fire_trial.py -- --help
NAME
    fire_trial.py

SYNOPSIS
    fire_trial.py <flags>

FLAGS
    --end_point=END_POINT

# ヘルプオプションなし
$ python fire_trial.py
NAME
    fire_trial.py

SYNOPSIS
    fire_trial.py - COMMAND | VALUE

COMMANDS
    COMMAND is one of the following:

     getticker

VALUES
    VALUE is one of the following:

     end_point
```
ヘルプ無しで`python fire_trial.py`と入力するとコマンドリストが表示されるのに、コマンドリストヘルプだとなぜか寂しい。縦に長く、表示が切れるとパッと見でわかりにくそう。オプション解説がないのも、ちょっとつらい。


# 個別コマンドヘルプ比較
## baker
```shell
$ python baker_trial.py bitflyer_getticker --help
Usage: baker_trial.py bitflyer_getticker [<product_code>] [<is_json>]

bitflyer api getticker

Options:

   --product_code  'BTC_JPY or BTC_ETH
   --is_json       return json
```
シンプル。オプションの解説があるのは、やっぱり落ち着く。

## click
```shell
$ python click_trial.py bitflyer-getticker --help
Usage: click_trial.py bitflyer-getticker [OPTIONS]

Options:
  -p, --product_code TEXT   BTC_JPY or BTC_ETH
  --is_json / --no-is_json  return json
  --help                    Show this message and exit.
```
シンプル。短縮版オプションがつかえるのが便利そう。

## fire
```shell
$ python fire_trial.py getticker -- --help
NAME
    fire_trial.py getticker

SYNOPSIS
    fire_trial.py getticker <flags>

FLAGS
    --product_code=PRODUCT_CODE
    --is_json=IS_JSON
```
少し縦長。オプション解説がないのも少し寂しい

# 個別まとめ(ドキュメントリンク付き)
## baker
[README.txt](https://bitbucket.org/mchaput/baker/src/default/README.txt)

↑ これしか見つからなかったので、とりあえずこれを参考にしました。
markdownじゃないので、ちょっと見にくい。。。(他に正式なドキュメントがあるのかも？)
シンプルだけど、機能は少なめな雰囲気。

## click
[Documentation](https://click.palletsprojects.com/en/7.x/)

機能も豊富にありそう。設定可能な項目が多い分、実装はほかよりも少し手間がかかりそうだけど、かゆいところに手が届きそうなのがぐっとくる。ドキュメントも充実。

## fire
[The Python Fire Guide](https://github.com/google/python-fire/blob/master/docs/guide.md)

実装が一番楽そう。機能もそこそこ充実。機能も豊富でネスティングに加えて、チェインコールやプロパティの表示にも対応。簡単実装で機能もそこそこ充実してるけど、オプションの解説設定ができなさそうなのが、けっこうつらい。ヘルプ表示も縦長で、ちょっと見ずらい。

# まとめ
かゆい所に手が届くclickと簡単実装と機能のバランスがいいfireで迷ったあげく、両方かな(笑)という結論に至りました。

とりあえずfireでコマンド化して、ヘルプを強化したくなったらclickに切り替えみたいな感じで、使ってみようと思います。

切り替えを想定して関数ベースで実装する事だけ気を付けて、しばらく試してみようと思います。
