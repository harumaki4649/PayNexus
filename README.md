# PayNexus

## プログラム言語

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [インストール方法](#インストール方法)
3. [環境](#環境)
4. [モジュールについて](#モジュールについて)

## プロジェクトについて

PythonからPaypayを操作できる非公式モジュールです。<br>
また、開発時間短縮のために以下のモジュールを参考・ベースに利用させていただいております。<br><br>
**ベースモジュール**<br>
・[PayPaython](https://github.com/taka-4602/PayPaython)<br>
・[paypay.py](https://github.com/yuki-1729/paypay.py)

## インストール方法
[こちらのPyPIパッケージ](https://pypi.org/project/PayNexus/)を、
```pip install PayNexus```
などのコマンドでインストールしてください。<br>
※お好みでバージョンを指定してください


## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.9.19     |

パッケージのバージョンは requirements.txt を参照してください

# モジュールについて
## タスク
- [x] ログイン機能
- [x] DiscordにWebhookを用いたログ等の送信
- [x] 自動再ログイン（UUIDが必要）
- [x] セッション保持機能のデータ保護（Paypayに登録された電話番号＋パスワードを用いて保護）
- [ ] Paypayリンクの自動処理(https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW でも処理できるようにします)
<!--- 必須マーク : <span style="color:red">＊</span> -->
## ドキュメント
| 関数                                                      | パラメータ                                                      | 説明                                                                                                                   |
|---------------------------------------------------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| PayPay                                           | **phone** -- str: 電話番号<span style="color:red">＊</span>     | これは例外で関数ではなく、`Class`                                                                                                   |
| PayNexusを利用するために必要（Discord.pyでいう```discord.Client()```） |                                                            |                                                                                                                      |
|                                                         | **password** -- str: パスワード<span style="color:red">＊</span> |                                                                                                                      |
|                                                         | **client_uuid** -- str: ログイン済み`client_uuid `               | login関数を使用してログインすると既存のログイン時のjsonに加え、`client_uuid`が追加されて返ってくるのでそちらをここで指定します                                           |
|                                                         | **session_save** -- str: ファイルパス                            | ログイン情報を保存するためのファイルパスを指定、拡張子はお任せ                                                                                      |
|                                                         | **debug** -- bool: `True` or `False`                       | デバッグメッセージの有効化と無効化（デフォルトでは`False`）                                                                                    |
|                                                         | **webhook** -- str: DiscordのWebhook                        | ログ等の送信に使用                                                                                                            |
|                                                         | **session_auto_save** -- bool: `True` or `False`           | セッションを自動で保持するかどうか（デフォルトでは`False`）                                                                                    |
|                                                         | **session_check_interval** -- int: 分単位で時間を指定               | セッション切れを確認する間隔、デフォルトでは3～7分の間                                                                                         |
|                                                         | **session_check_interval_delay** -- list: `[min, max]`     | minとmaxは秒単位で、min～maxの中からランダムな時間を`session_check_interval`に足す。また、デフォルトでは`[0, 0]'（アカウントが凍結されないようにする願いが込められているが、おそらく関係ない） |
| login                                                   | **otp** -- str:受信したワンタイムパスワード                              | Paypayアカウントにログイン                                                                                                     |
| resend_otp                                              |                                                            | 認証コードを再送信                                                                                                            |

## 使用例
```python
import PayNexus

Nexus = PayNexus.PayPay(phone="",
                        password="",
                        client_uuid="",
                        session_save="",
                        debug=True,
                        webhook="",
                        session_auto_save=True,
                        # 時間は分単位（0.1で6秒）
                        session_check_interval=3,
                        #時間は秒単位 [min, max]
                        session_check_interval_delay=[0, 180])

#ログイン
paypay = PayNexus.PayPay(phone="08012345678",
                         password="Test-1234")  #ログイン済みclient_uuid="str"をセットするとOTPをパスできます #token="str"トークンをセットするとログインをパスします #proxy=dictでプロキシを設定できます
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

※機能説明はリリースまでには完成させます（一部機能しか書いてません）
※タスクが完了していてもモジュールが更新されていない場合がございます（その際は時間を空けてご確認ください）
