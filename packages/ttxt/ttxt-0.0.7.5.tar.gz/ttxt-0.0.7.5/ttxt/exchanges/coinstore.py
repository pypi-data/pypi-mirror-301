from email import header
import hmac
import base64
import hashlib
import json
import time
import urllib.parse
import requests
from urllib.parse import urlencode
from ttxt.utils import general
from ttxt.base import baseSpotExchange
from ttxt.types import baseTypes
import uuid
import math

class coinstore(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.key = key.encode('utf-8')
        self.secret = secret.encode('utf-8')
        self.domain_url = "https://api.coinstore.com"
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "")
    
    def _getUserSymbol(self, symbol):
        raise NotImplementedError("Not implemented")
    
    def get_timstamp(self):
        return int(time.time()*1000)

    ## Auth 
    def parse_params_to_str(self, params):
        params = [(key, val) for key, val in params.items()]
        params.sort(key=lambda x:x[0])
        url = "?" + urlencode(params)
        if url == '?':
            return ''
        return url

    def create_signature(self, expires, payload=None, queryString=None):
        expires_key = str(math.floor(expires / 30000))
        expires_key = expires_key.encode("utf-8")
        key = hmac.new(self.secret, expires_key, hashlib.sha256).hexdigest()
        key = key.encode("utf-8")
        if not payload:
            payload = json.dumps({})
        if queryString:
            payload = queryString.encode("utf-8")
        else:
            payload = json.dumps(payload).encode("utf-8")
        signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
        return signature, payload

    def _signedRequest(self, method, request_path, body=None, queryString=None):
        expires = self.get_timstamp()
        sig, payload = self.create_signature(expires,payload=body, queryString=queryString)
        headers = {
            'X-CS-APIKEY':self.key,
            'X-CS-SIGN':sig,
            'X-CS-EXPIRES':str(expires),
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        url = self.domain_url + request_path
        if queryString:
            url += f"?{queryString}"
            payload = None  # set to none for fetch trades
        if method == "POST":
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                return response.json()
            except Exception as e:
                raise e
        if method == "GET":
            try:
                response = requests.request("GET", url, headers=headers, data=payload)
                return response.json()
            except Exception as e:
                raise e
    
    def _unsignedRequest(self, method, apiUrl, params):
        url = self.domain_url + apiUrl
        if method == 'GET':
            try:
                response = requests.request('get', url, params=params)
                return response.json()
            except Exception as e:
                raise e
        else:
            raise Exception(f"{method} Method not supported for unsigned calls")
    
    ## parsers
    def _parseBalance(self, balData):
        parsedBal = {"free": {}, "total": {}}
        if balData["code"] != 0:
            raise Exception(balData['message'])
        data = balData.get("data", [])
        for d in data:
            if d["typeName"] == "FROZEN":
                if d["currency"] not in parsedBal["total"]:
                    parsedBal["total"][d["currency"]] = 0
                parsedBal["total"][d["currency"]] += float(d["balance"])
            if d["typeName"] == "AVAILABLE":
                parsedBal["free"][d["currency"]] = float(d["balance"])
                parsedBal["total"][d["currency"]] += float(d["balance"])
        return parsedBal
    
    def _parseCreateorder(self, order):
        if order["code"] != 0:
            raise Exception(order['message'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        if "data" in order and order["data"] != {}:
            parsedOrder['id'] = order['data']['ordId']
            parsedOrder["orderJson"] = json.dumps(order)
        return parsedOrder
    
    def _parseOpenOrders(self, orders):
        if orders["code"] != 0:
            raise Exception(orders['message'])
        parsedOrderList = []    
        if "data" in orders and orders['data'] != {}:
            for orderJson in orders["data"]:
                currentOrder = {} 
                currentOrder["id"] = orderJson["ordId"]
                currentOrder["symbol"] = orderJson["symbol"]
                currentOrder["price"] = orderJson["ordPrice"]
                currentOrder["amount"] = orderJson["ordQty"]
                currentOrder["side"] = orderJson["side"]
                currentOrder["timestamp"] = orderJson["timestamp"]
                currentOrder["status"] = orderJson["ordStatus"]
                currentOrder["orderJson"] = json.dumps(orderJson)
                parsedOrderList.append(currentOrder)
        return parsedOrderList
    
    def _parseFetchOrder(self, data):
        parsedOrder = {"id": None, "symbol": None, "price": None, "amount": None, "takerOrMaker": None, "datetime": None, "fee": None, "fee_currency": None,
                       "side": None, "timestamp": None, "status": None}
        if data != {}:
            order = data["data"]
            parsedOrder["id"] = order["orderId"]
            parsedOrder["tradeId"] = order["tradeId"]
            parsedOrder["symbol"] = "" # not returned in response 
            parsedOrder["price"] = order["execAmt"] / order["execQty"]  # price not returned in response 
            parsedOrder['takerOrMaker'] = "taker" if order["role"] == 1 else "maker"
            parsedOrder["amount"] = order["execQty"]
            parsedOrder["side"] = "buy" if order["side"] == 1 else "sell"
            parsedOrder["timestamp"] = order["matchTime"] * 1000  # ms epoch
            parsedOrder["datetime"] = general.ts_to_datetime(parsedOrder["timestamp"])
            parsedOrder["status"] = "closed"
            parsedOrder['fee'] = order.get("fee", None)
            parsedOrder["fee_currency"] = "quoteCurrency"  # not possible to split pair to get correct quote currency 
        return parsedOrder
    
    def _parseFetchTrades(self, orders):
        if orders["code"] != 0:
            raise Exception(orders['message'])
        parsedTradesList = []
        for orderJson in orders["data"]:
            parsedTradesList.append(self._parseFetchOrder({'data': orderJson}))
        return parsedTradesList
    
    def _parseCancelOrder(self, order):
        if order["code"] != 0:
            raise Exception(order['message'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        if "data" in order and order["data"] != {}:
            parsedOrder['id'] = order['data']['ordId']
            parsedOrder["orderJson"] = json.dumps(order)
        return parsedOrder
    
    ## Exchange functions 
    def fetch_ticker(self, symbol):
        raise NotImplementedError("method not implemented")
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = "/api/spot/accountList"
        try:
            resp = self._signedRequest('POST', apiUrl, params)
            return self._parseBalance(resp)
        except Exception as e:
            raise e
        
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}): 
        apiUrl = "/api/trade/match/accountMatches"
        try:
            params = f"symbol={self._getSymbol(symbol).lower()}"
            response = self._signedRequest('GET', request_path=apiUrl, queryString=params)
            return self._parseFetchTrades(response)
        except Exception as e:
            raise e
    
    def create_order(self, symbol, side, amount, order_type, price=None, params={}): 
        if order_type == "limit":
            return self.create_limit_order(symbol, side, amount, price, params)
        elif order_type == "market":
            return self.create_market_order(symbol, side, amount, params)
        else: raise Exception("wrong order type, only supports market and limit")
    
    def create_market_order(self, symbol, side, amount, params={}):
        apiUrl = "/api/trade/order/place"
        body = {
            "symbol": self._getSymbol(symbol),
            "side": side.upper(),
            "ordType": "MARKET",
        }
        if side == "sell":
           body["ordQty"] = str(amount)
        else:
           body["ordAmt"] = str(amount)
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body)
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, side, amount, price, params={}):
        apiUrl = "/api/trade/order/place"
        body = {
            "symbol": self._getSymbol(symbol),
            "side": side.upper(),
            "ordType": "LIMIT",
            "ordPrice": str(price),
            "ordQty": str(amount)
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body)
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def cancel_order(self, id=None, symbol=None, params={}):
        apiUrl = "/api/trade/order/cancel"
        try:
            body = {
                "ordId": int(id),
                "symbol":self._getSymbol(symbol)
            }
            response = self._signedRequest('POST', request_path=apiUrl,body=body)
            return self._parseCancelOrder(response)
        except Exception as e:
            raise e
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        apiUrl = "/api/trade/order/active"
        try:
            response = self._signedRequest('GET', request_path=apiUrl, body=None)
            return self._parseOpenOrders(response)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol = None, params={}):
        raise NotImplementedError("method not supported")