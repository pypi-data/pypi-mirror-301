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

class coinbase(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.domain_url = "https://api.coinbase.com"
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "")
    
    def _getUserSymbol(self, symbol):
        raise NotImplementedError("Not implemented")
    
    def get_timstamp(self):
        return str(time.time())

    ## Auth 
    def parse_params_to_str(self, params):
        params = [(key, val) for key, val in params.items()]
        params.sort(key=lambda x:x[0])
        url = "?" + urlencode(params)
        if url == '?':
            return ''
        return url

    def get_auth_headers(self, message):
        if not message or message == {}:
            message = ''
        message = message.encode('ascii')
        hmac_key = base64.b64decode(self.secret)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
        return {
            'Content-Type': 'Application/JSON',
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': self.get_timstamp(),
            'CB-ACCESS-KEY': self.key
        }

    def _signedRequest(self, method, request_path, body=None, queryString=None):
        headers = self.get_auth_headers(message=body)
        url = self.domain_url + request_path
        if queryString:
            url += f"?{queryString}"
        if method == "POST":
            try:
                response = requests.request("POST", url, headers=headers, data=body)
                return response.json()
            except Exception as e:
                raise e
        if method == "GET":
            try:
                response = requests.request("GET", url, headers=headers)
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
            parsedOrder["price"] = 0 # not returned in response
            parsedOrder['takerOrMaker'] = order["role"].lower()
            parsedOrder["amount"] = order["execQty"]
            parsedOrder["side"] = order["side"]
            parsedOrder["timestamp"] = int(order["ts"])  # ms epoch
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
        apiUrl = "/api/v3/brokerage/accounts"
        try:
            resp = self._signedRequest('GET', apiUrl)
            return resp #self._parseBalance(resp)
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