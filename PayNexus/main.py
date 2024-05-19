"""BSD 2-Clause License

Copyright (c) 2024, harumaki4649

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
import os.path
import random
import time

import requests
import datetime
import uuid
import pickle
import threading
# pip install term-printer (https://qiita.com/nanato12/items/5f287f3008135ca4cb03)
from term_printer import Color, cprint
# pip install discord-webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
from .Colors import *
from cryptography.fernet import Fernet
import hashlib
import base64

headers = {
    "Accept": "application/json, text/plain, */*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    "Content-Type": "application/json"
}


class PayPayLoginError(Exception):
    pass


class PayPayPasswordError(Exception):
    pass


class PayPayError(Exception):
    pass


def generate_key(phone_number, password):
    # 電話番号とパスワードを結合してハッシュ化する
    key = hashlib.sha256((phone_number + password).encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data


def convert_to_paypay_code_format(pcode):
    if pcode.startswith("https://pay.paypay.ne.jp/"):
        return pcode.split('/')[-1]
    elif pcode.startswith("[PayPay]"):
        start_index = pcode.find("https://pay.paypay.ne.jp/")
        if start_index != -1:
            url = pcode[start_index:]
            return url.split('/')[-1]
    return pcode


class PayPay:
    def __init__(self, phone: str = None, password: str = None, client_uuid: str = str(uuid.uuid4()), token: str = None,
                 proxy: dict = None, session_save="./paypay_login.date", debug=False, webhook=None,
                 session_auto_save=False, session_check_interval=random.randint(3, 7),
                 session_check_interval_delay=[0, 0]):
        self.session = requests.Session()
        self.proxy = proxy
        self.uuuid = client_uuid
        self.phone = phone
        self.pas = password
        self.debug = debug
        self.webhook = webhook
        self.session_save = session_save
        self.key = generate_key(phone, password)
        self.session_auto_save = session_auto_save
        if os.path.exists(session_save) and token is None:
            with open(session_save, 'rb') as f:
                token = decrypt_data(pickle.load(f), self.key)
            self.token = token
            self.session.cookies.set("token", token)
            try:
                if not self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo", headers=headers,
                                        proxies=self.proxy, timeout=(10, 5)).ok:
                    self.color_print(f"ログイン失敗", [Color.RED])
                    token = None
            except Exception:
                self.color_print(f"ログイン失敗", [Color.RED])
                token = None
        if token is None:
            loginj = {
                "scope": "SIGN_IN",
                "client_uuid": self.uuuid,
                "grant_type": "password",
                "username": self.phone,
                "password": self.pas,
                "add_otp_prefix": True,
                "language": "ja"
            }
            login = self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token", json=loginj, headers=headers,
                                      proxies=proxy)
            try:
                self.token = (login.json()["access_token"])
                with open(session_save, "wb") as f:
                    pickle.dump(encrypt_data(self.token, self.key), f)
            except:
                try:
                    if login.json()["response_type"] == "ErrorResponse":
                        raise PayPayLoginError(login.json())
                    else:
                        self.pre = login.json()["otp_prefix"]
                        self.refid = login.json()["otp_reference_id"]
                except:
                    raise PayPayLoginError(login.text)
        else:
            self.session.cookies.set("token", token)
            try:
                if not self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo", headers=headers,
                                        proxies=self.proxy, timeout=(10, 5)).ok:
                    raise "ログインに失敗"
            except Exception as e:
                self.color_print(f"ログイン失敗", [Color.RED])
                raise e
        if session_auto_save:
            thread = threading.Thread(target=self.session_auto_saver, kwargs={"interval": session_check_interval,
                                                                              "delay": session_check_interval_delay})
            thread.setDaemon(True)
            thread.start()
            return

    def login(self, otp: str):
        otpj = {
            "scope": "SIGN_IN",
            "client_uuid": self.uuuid,
            "grant_type": "otp",
            "otp_prefix": self.pre,
            "otp": otp,
            "otp_reference_id": self.refid,
            "username_type": "MOBILE",
            "language": "ja"
        }

        try:
            try:
                login = self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token", json=otpj, headers=headers,
                                          proxies=self.proxy, timeout=(10, 10)).json()
            except Exception as e:
                self.color_print(f"ログイン失敗", [Color.GREEN])
                raise e
            self.token = (login["access_token"])
            with open(self.session_save, "wb") as f:
                pickle.dump(encrypt_data(self.token, self.key), f)
        except:
            self.color_print(f"ログイン失敗", [Color.GREEN])
            raise PayPayLoginError(login)
        login.update({"client_uuid": str(self.uuuid)})
        self.color_print(f"ログイン完了", [Color.GREEN])
        return login

    def resend_otp(self, otp_reference_id: str):
        resendj = {
            "add_otp_prefix": "true"
        }
        resend = self.session.post(f"https://www.paypay.ne.jp/app/v1/otp/mobile/resend/{otp_reference_id}",
                                   json=resendj, headers=headers, proxies=self.proxy)
        try:
            self.pre = resend.json()["otp_prefix"]
            self.refid = resend.json()["otp_reference_id"]
        except:
            raise PayPayLoginError(resend.json())
        return resend.json()

    def balance(self) -> dict:
        balance = self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo", headers=headers,
                                   proxies=self.proxy)
        if balance.json()["header"]["resultCode"] != "S0000":
            raise PayPayError(balance.json()["header"]["resultCode"], balance.json()["header"]["resultMessage"])
        paypay_zandaka = str(balance.json()["payload"]["walletSummary"]["usableBalanceInfoWithoutCashback"]["balance"])
        embed = DiscordEmbed(title="Paypay残高", description=f"{paypay_zandaka}円",
                             color=Color.green().value)
        thread = threading.Thread(target=self.webhook_send, kwargs={"embed": embed, "response": balance})
        thread.start()
        return balance.json()

    def user_info(self) -> dict:
        uinfo = self.session.get("https://www.paypay.ne.jp/app/v1/getUserProfile?", headers=headers, proxies=self.proxy)
        embed = DiscordEmbed(title="ユーザー情報", description=str(uinfo.json()),
                             color=Color.green().value)
        thread = threading.Thread(target=self.webhook_send, kwargs={"embed": embed, "response": uinfo})
        thread.start()
        return uinfo.json()

    def display_info(self) -> dict:
        dinfo = self.session.get("https://www.paypay.ne.jp/app/v2/bff/getProfileDisplayInfo", headers=headers,
                                 proxies=self.proxy)
        data = dinfo.json()
        print(data)
        data = data["payload"]["userProfile"]
        new_json = {
            'displayName': data['displayName'],
            'nickName': data['nickName'],
            'lastName': data['lastName'],
            'firstName': data['firstName'],
            'lastNameKana': data['lastNameKana'],
            'firstNameKana': data['firstNameKana'],
            'lastNameRomaji': data['lastNameRomaji'],
            'firstNameRomaji': data['firstNameRomaji']
        }
        print(str(new_json))
        embed = DiscordEmbed(title="ディスプレイ情報", description=str(new_json),
                             color=Color.green().value)
        thread = threading.Thread(target=self.webhook_send, kwargs={"embed": embed, "response": dinfo})
        thread.start()
        return dinfo.json()

    def payment_method(self) -> dict:
        payment = self.session.get("https://www.paypay.ne.jp/app/v2/bff/getPaymentMethodList", headers=headers,
                                   proxies=self.proxy)
        data = payment.json()["payload"]["paymentMethodList"]
        embed = DiscordEmbed(title="ペイメントメソッド", description=str(data),
                             color=Color.green().value)
        thread = threading.Thread(target=self.webhook_send, kwargs={"embed": embed, "response": payment})
        thread.start()
        return payment.json()

    def history(self) -> dict:
        history = self.session.get("https://www.paypay.ne.jp/app/v2/bff/getPay2BalanceHistory", headers=headers,
                                   proxies=self.proxy)
        embed = DiscordEmbed(title="履歴", description=str(history.json()),
                             color=Color.green().value)
        thread = threading.Thread(target=self.webhook_send, kwargs={"embed": embed, "response": history})
        thread.start()
        return history.json()

    def create_link(self, kingaku: int, password: str = "none") -> dict:
        try:
            if not len(password) == 4:
                raise PayPayPasswordError("パスワードの値がおかしいです！")
            if not password == "none":
                int(password)
        except:
            raise PayPayPasswordError("パスワードの値がおかしいです！")
        clink = {
            "androidMinimumVersion": "3.45.0",
            "requestId": str(uuid.uuid4()),
            "requestAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(
                '%Y-%m-%dT%H:%M:%S+0900'),
            "theme": "default-sendmoney",
            "amount": kingaku,
            "iosMinimumVersion": "3.45.0"
        }

        if not password == "none":
            clink["passcode"] = password

        createlink = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/executeP2PSendMoneyLink",
                                       headers=headers, json=clink, proxies=self.proxy)
        return createlink.json()

    def check_link(self, pcode: str) -> dict:
        info = self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={convert_to_paypay_code_format(pcode)}",
                                headers=headers, proxies=self.proxy)
        embed = DiscordEmbed(title="リンクチェック", description=str(info.json()),
                             color=Color.green().value)
        thread = threading.Thread(target=self.webhook_send, kwargs={"embed": embed, "response": info})
        thread.start()
        return info.json()

    def receive(self, pcode: str, password: str = "4602", info: dict = None) -> dict:
        try:
            if not len(password) == 4:
                raise PayPayPasswordError("パスワードの値がおかしいです！")
            int(password)
        except:
            raise PayPayPasswordError("パスワードの値がおかしいです！")
        if info == None:
            info = self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={convert_to_paypay_code_format(pcode)}",
                                    headers=headers, proxies=self.proxy).json()
        recevej = {
            "verificationCode": convert_to_paypay_code_format(pcode),
            "client_uuid": self.uuuid,
            "passcode": password,
            "requestAt": str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(
                '%Y-%m-%dT%H:%M:%S+0900')),
            "requestId": info["payload"]["message"]["data"]["requestId"],
            "orderId": info["payload"]["message"]["data"]["orderId"],
            "senderMessageId": info["payload"]["message"]["messageId"],
            "senderChannelUrl": info["payload"]["message"]["chatRoomId"],
            "iosMinimumVersion": "3.45.0",
            "androidMinimumVersion": "3.45.0"
        }

        rece = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/acceptP2PSendMoneyLink", json=recevej,
                                 headers=headers, proxies=self.proxy)
        embed = DiscordEmbed(title="受け取り", description=str(rece.json()),
                             color=Color.green().value)
        thread = threading.Thread(target=self.webhook_send, kwargs={"embed": embed, "response": rece})
        thread.start()
        return rece.json()

    def reject(self, pcode: str, info: dict = None) -> dict:
        if info == None:
            info = self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={convert_to_paypay_code_format(pcode)}",
                                    headers=headers, proxies=self.proxy).json()
        rejectj = {
            "requestAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(
                '%Y-%m-%dT%H:%M:%S+0900'),
            "orderId": info["payload"]["pendingP2PInfo"]["orderId"],
            "verificationCode": convert_to_paypay_code_format(pcode),
            "requestId": str(uuid.uuid4()),
            "senderMessageId": info["payload"]["message"]["messageId"],
            "senderChannelUrl": info["payload"]["message"]["chatRoomId"],
            "iosMinimumVersion": "3.45.0",
            "androidMinimumVersion": "3.45.0",
            "client_uuid": self.uuuid
        }

        reje = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/rejectP2PSendMoneyLink", json=rejectj,
                                 headers=headers, proxies=self.proxy)
        return reje.json()

    def send_money(self, kingaku: int, external_id: str) -> dict:
        sendj = {
            "theme": "default-sendmoney",
            "externalReceiverId": external_id,
            "amount": kingaku,
            "requestId": str(uuid.uuid4()),
            "requestAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime(
                '%Y-%m-%dT%H:%M:%S+0900'),
            "iosMinimumVersion": "3.45.0",
            "androidMinimumVersion": "3.45.0"
        }
        send = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/executeP2PSendMoney", headers=headers,
                                 json=sendj, proxies=self.proxy)
        return send.json()

    def create_p2pcode(self) -> dict:
        cp2c = self.session.post("https://www.paypay.ne.jp/app/v1/p2p-api/createP2PCode", headers=headers,
                                 proxies=self.proxy)
        return cp2c.json()

    def create_payment_otcfh(self) -> dict:
        cpotcj = {
            "paymentMethodType": "WALLET",
            "paymentMethodId": "106177237",
            "paymentCodeSessionId": str(uuid.uuid4()),
        }
        cpotc = self.session.post("https://www.paypay.ne.jp/app/v2/bff/createPaymentOneTimeCodeForHome",
                                  headers=headers, proxies=self.proxy, json=cpotcj)
        return cpotc.json()

    def session_auto_saver_exit(self):
        self.session_auto_save = False
        return

    def session_auto_saver(self, interval, delay):
        min_d, max_d = delay
        from term_printer import Color
        if self.uuuid is None:
            self.color_print(f"自動再ログイン機能はuuid(client_uuid)が指定されていないため利用できません",
                             [Color.YELLOW])
            return
        interval = interval * 60
        while self.session_auto_save:
            self.session.cookies.set("token", self.token)
            try:
                if not self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo", headers=headers,
                                        proxies=self.proxy, timeout=(10, 5)).ok:
                    raise
                self.color_print(f"セッションに異常なし", [Color.GREEN])
            except Exception:
                self.color_print(f"再ログイン開始", [Color.RED])
                if self.token is None:
                    loginj = {
                        "scope": "SIGN_IN",
                        "client_uuid": self.uuuid,
                        "grant_type": "password",
                        "username": self.phone,
                        "password": self.pas,
                        "add_otp_prefix": True,
                        "language": "ja"
                    }
                    login = self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token", json=loginj,
                                              headers=headers,
                                              proxies=self.proxy)
                    try:
                        self.token = (login.json()["access_token"])
                        with open(self.session_save, "wb") as f:
                            pickle.dump(encrypt_data(self.token, self.key), f)
                    except:
                        try:
                            if login.json()["response_type"] == "ErrorResponse":
                                raise PayPayLoginError(login.json())
                            else:
                                self.pre = login.json()["otp_prefix"]
                                self.refid = login.json()["otp_reference_id"]
                        except:
                            raise PayPayLoginError(login.text)
                else:
                    self.session.cookies.set("token", self.token)
                    try:
                        if not self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo", headers=headers,
                                                proxies=self.proxy, timeout=(10, 5)).ok:
                            raise "ログインに失敗"
                        self.color_print(f"ログイン成功", [Color.GREEN])
                    except Exception as e:
                        self.color_print(f"ログイン失敗", [Color.RED])
                        raise e
            delay = random.randint(min_d, max_d)
            # whileは自動で終わるようにしたけど、time.sleepが終わるまでwhileのif checkがされないから何とかする
            time.sleep(interval + delay)

    def color_print(self, text, color):
        if self.debug:
            cprint(text, attrs=color)

    def webhook_send(self, text=None, embed=None, response=None):
        if self.webhook is None or response is None:
            return None
        if not response.ok:
            return None
        if text is None and embed is None:
            return None
        elif text is None and not embed is None:
            webhook = DiscordWebhook(url=self.webhook, rate_limit_retry=True)
            webhook.add_embed(embed)
            response = webhook.execute()
        elif not text is None and not embed is None:
            webhook = DiscordWebhook(url=self.webhook, rate_limit_retry=True, content=text)
            webhook.add_embed(embed)
            response = webhook.execute()
        elif not text is None and embed is None:
            webhook = DiscordWebhook(url=self.webhook, rate_limit_retry=True, content=text)
            response = webhook.execute()
        else:
            self.color_print("Webhookの関数に欠陥があります。\n開発者にお問い合わせください。", [Color.YELLOW])
            return None
        return response


class Pay2:
    def __init__(self, proxy: dict = None):
        self.proxy = proxy

    def check_link(self, pcode: str) -> dict:
        info = requests.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={convert_to_paypay_code_format(pcode)}",
                            headers=headers, proxies=self.proxy)
        return info.json()
