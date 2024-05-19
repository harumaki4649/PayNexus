# PayNexus

## 目次

>1. [プロジェクトについて](#プロジェクトについて)
>2. [インストール方法](#インストール方法)
>3. [環境](#環境)
>4. [モジュールについて](#モジュールについて)

## プロジェクトについて

PythonからPaypayを操作できる非公式モジュールです。<br>
また、開発時間短縮のために以下のモジュールを参考・ベースに利用させていただいております。<br><br>
>**ベースモジュール**<br>
・[PayPaython](https://github.com/taka-4602/PayPaython)<br>
・[paypay.py](https://github.com/yuki-1729/paypay.py)
<br><br>**公式サイト**<br>
・[公式Github（使い方など）はこちら](https://github.com/harumaki4649/PayNexus)<br>
・[公式Note（更新情報など）はこちら](https://note.com/humareuka6295/m/m0fc09a1b95c1)


## インストール方法
>[こちらのPyPIパッケージ](https://pypi.org/project/PayNexus/)を、
```pip install PayNexus```
などのコマンドでインストールしてください。<br>
※お好みでバージョンを指定してください


## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.9.19     |

>モジュール（パッケージ）のバージョンは requirements.txt を参照してください

# モジュールについて
## タスク
- [x] ログイン機能
- [x] DiscordにWebhookを用いたログ等の送信
- [x] 自動再ログイン（UUIDが必要）
- [x] セッション保持機能のデータ保護（Paypayに登録された電話番号＋パスワードを用いて保護）
- [x] Paypayリンクの自動処理(https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW などでも処理できるようにします)
- [ ] `create_link`と`send_money`が動作しない問題の修正（使用するAPIを変える必要があるため検討中）
<!--- 必須マーク : <span style="color:red">＊</span> -->
## ドキュメント
| 関数                         | パラメータ                                                                                                                  | 説明                                                                                                                         |
|----------------------------|------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| PayPay                     | **phone** -- str: 電話番号<span style="color:red">＊</span>                                                                 | これは例外で関数ではなく、`Class`です。また、PayNexusを利用するために必要（Discord.pyでいう```discord.Client()```のようなものです）                                  |
|                            | **password** -- str: パスワード<span style="color:red">＊</span>                                                             |                                                                                                                            |
|                            | **client_uuid** -- str: ログイン済み`client_uuid `                                                                           | login関数を使用してログインすると既存のログイン時のjsonに加え、`client_uuid`が追加されて返ってくるのでそちらをここで指定します                                                 |
|                            | **session_save** -- str: ファイルパス                                                                                        | ログイン情報を保存するためのファイルパスを指定、拡張子はお任せ                                                                                            |
|                            | **debug** -- bool: `True` or `False`                                                                                   | デバッグメッセージの有効化と無効化（デフォルトでは`False`）                                                                                          |
|                            | **webhook** -- str: DiscordのWebhook                                                                                    | ログ等の送信に使用                                                                                                                  |
|                            | **session_auto_save** -- bool: `True` or `False`                                                                       | セッションを自動で保持するかどうか（デフォルトでは`False`）                                                                                          |
|                            | **session_check_interval** -- int: 分単位で時間を指定                                                                           | セッション切れを確認する間隔、デフォルトでは3～7分の間                                                                                               |
|                            | **session_check_interval_delay** -- list: `[min, max]`                                                                 | minとmaxは秒単位で、min～maxの中からランダムな時間を`session_check_interval`に足す。また、デフォルトでは`[0, 0]'（アカウントが凍結されないようにする願いが込められているが、おそらく関係ない）      |
| login                      | **otp** -- str:受信したワンタイムパスワード<span style="color:red">＊</span>                                                          | Paypayアカウントにログイン                                                                                                           |
| resend_otp                 | **otp_reference_id** -- str: `paypay.refid`<span style="color:red">＊</span>                                            | 認証コードを再送信します。`paypay.refid`はPayPayクラスを利用すると利用可能（例：```paypay = PayNexus.PayPay(phone="08012345678",password="Test-1234"```） |
| check_link                 | **pcode** -- str: 送金リンクのコード<span style="color:red">＊</span>                                                            | 送金リンクの金額などを取得（ログイン必要）                                                                                                      |
| PayNexus.Pay2().check_link | **pcode** -- str: 送金リンクのコード<span style="color:red">＊</span>                                                            | 送金リンクの金額などを取得（ログイン不要）                                                                                                      |
| receive                    | **pcode** -- str: 送金リンクのコード<span style="color:red">＊</span>                                                            | 送金リンクを介して受け取り                                                                                                              |
| reject                     | **pcode** -- str: 送金リンクのコード<span style="color:red">＊</span>                                                            | 送金の受け取りを辞退                                                                                                                 |
| create_link                | **kingaku** -- int: 金額<span style="color:red">＊</span> **password** -- str: 4桁のパスワード                                   | 送金リンクを作成                                                                                                                   |
| balance                    |                                                                                                                        | 残高を取得                                                                                                                      |
| user_info                  |                                                                                                                        | ユーザー情報を取得                                                                                                                  |
| display_info               |                                                                                                                        | ディスプレイ情報を取得                                                                                                                |
| payment_method             |                                                                                                                        | 支払い方法を取得                                                                                                                   |
| history                    |                                                                                                                        | 取引履歴を取得                                                                                                                    |
| send_money                 | **kingaku** -- int: 金額<span style="color:red">＊</span> **external_id** -- str: ユーザーのid<span style="color:red">＊</span> | 指定した`external_id`のユーザーに直接送金                                                                                                |
| create_p2pcode             |                                                                                                                        | 送金してもらうためのURLを作成する(PayPayアプリのQRコードとおなじ)                                                                                    |
| create_payment_otcfh       |                                                                                                                        | 支払いのワンタイムコードを作成する(ホーム画面にあるあのバーコードとおなじ)                                                                                     |

## 使用例
```python
import PayNexus

# ログイン
paypay = PayNexus.PayPay(phone="電話番号",
                        password="パスワード",
                        client_uuid="uuid",
                        session_save="ファイルパス",
                        debug=True,
                        webhook="Discord Webhook",
                        session_auto_save=True,
                        # 時間は分単位（0.1で6秒）
                        session_check_interval=3,
                        #時間は秒単位 [min, max]
                        session_check_interval_delay=[0, 180])

otp = input(f"SMSに届いた番号:{paypay.pre}-")
print(paypay.login(otp))  #uuid確認用に["client_uuid"]にわざとuuidくっつけてます
#SMSの認証番号を再送
print(paypay.resend_otp(paypay.refid))  #refidの使い道ができた
otp = input(f"SMSに届いた番号:{paypay.pre}-")  #もっかい入力
print(paypay.login(otp))
#送金リンク確認
print(paypay.check_link("osuvUuLmQH8WA4kW"))  #ぺいぺい送金リンクの https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW <-ここね
#or
print(PayNexus.Pay2().check_link("osuvUuLmQH8WA4kW"))  #ログインなしでcheck_linkを使えるPay2クラスです #これもproxy=dictでプロキシを設定できる
#送金リンク受け取り
print(paypay.receive("osuvUuLmQH8WA4kW"))  #パスワードはpassword=str #事前にcheck_linkして返ってきたdictを引数infoに入れるとそのdictを使うようになります
#送金リンクを辞退
print(paypay.reject("osuvUuLmQH8WA4kW"))  #これもinfoにdictつっこめる
#送金リンクを作成
print(paypay.create_link(kingaku=1, password="1111"))  #パスワードはpassword=str
#残高確認
print(paypay.balance())
#ユーザー情報
print(paypay.user_info())
#ユーザーの表示情報
print(paypay.display_info())
#ユーザーの支払い方法
print(paypay.payment_method())
#取引履歴
print(paypay.history())
#指定したexternalidのユーザーに直接送金
print(paypay.send_money(kingaku=1, external_id="048f4fef00bdbad00"))  #このexternal_idはてきとーです
#送金してもらうためのURLを作成する(PayPayアプリのQRコードとおなじ)
print(paypay.create_p2pcode())
#支払いのワンタイムコードを作成する(ホーム画面にあるあのバーコードとおなじ)
print(paypay.create_payment_otcfh())

```

※タスクが完了していてもモジュールが更新されていない場合がございます（その際は時間を空けてご確認ください）
