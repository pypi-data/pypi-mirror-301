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

class blofin(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, password, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.password = password
        self.domain_url = "https://api.blofin.com"
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "-")
    
    def _getUserSymbol(self, symbol):
        return symbol.replace("-", "/")
    
    def get_uuid(self):
        return str(uuid.uuid4())
    
    def get_timstamp(self):
        return str(int(time.time()*1000))

    ## Auth 
    def parse_params_to_str(self, params):
        params = [(key, val) for key, val in params.items()]
        params.sort(key=lambda x:x[0])
        url = "?" + urlencode(params)
        if url == '?':
            return ''
        return url

    def create_signature_blofin(self, nonce, method, timestamp, path, queryString=None, body=None):
        # If it is a GET request, the body must be "".
        if body:
            prehash_string = f"{timestamp}{method}{path}{body or ''}{nonce}"
        elif queryString:
            prehash_string = f"{timestamp}{method}{path}{json.dumps(queryString) or ''}{nonce}"
        else:
            prehash_string = f"{path}{method}{timestamp}{nonce}"
        sign = base64.b64encode(hmac.new(self.secret.encode(), prehash_string.encode(),hashlib.sha256).hexdigest().encode()).decode()
        return sign

    def _signedRequest(self, method, request_path, queryString=None, body=None):
        body = json.dumps(body)
        ts = self.get_timstamp()
        nonce = self.get_uuid()
        if queryString and queryString != '':
            request_path += self.parse_params_to_str(queryString)
        headers = {
            "ACCESS-KEY": self.key,
            "ACCESS-SIGN": self.create_signature_blofin(nonce, method, ts, request_path, queryString, body),
            "ACCESS-TIMESTAMP": ts,
            "ACCESS-NONCE": nonce,
            "ACCESS-PASSPHRASE": self.password,
            "Content-Type": "application/json"
        }
        url = self.domain_url + request_path
        if method == "POST":
            try:
                response = requests.post(url, headers=headers, data=body)
                print(response)
                return response.json()
            except Exception as e:
                raise e
        if method == "GET":
            try:
                response = requests.get(url, headers=headers)
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
        if balData["code"] != 200:
            raise Exception(balData['msg'])
        data = balData.get("data", [])
        for d in data['balances']:
            parsedBal["free"][d["currency"]] = d["available"]
            parsedBal["total"][d["currency"]] = d["total"]
        return parsedBal
    
    def _parseCreateorder(self, order):
        print(order)
        if order["code"] != 200:
            raise Exception(order['msg'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        parsedOrder['id'] = order['data']['order_id']
        parsedOrder["orderJson"] = json.dumps(order['data'])
        return parsedOrder
    
    def _parseOpenOrders(self, orders):
        if orders["code"] != 200:
            raise Exception(orders['msg'])
        parsedOrderList = []    
        if "data" in orders and len(orders["data"]):
            for orderJson in orders["data"]:
                currentOrder = {} 
                currentOrder["id"] = orderJson["order_id"]
                currentOrder["symbol"] = orderJson["symbol"]
                currentOrder["price"] = float(orderJson["price"])
                currentOrder["amount"] = float(orderJson["quantity"])
                currentOrder["side"] = orderJson["order_side"]
                currentOrder["timestamp"] = orderJson["create_time"]
                currentOrder["status"] = orderJson["state"]
                currentOrder["orderJson"] = json.dumps(orderJson)
                parsedOrderList.append(currentOrder)
        return parsedOrderList
    
    def _parseFetchOrder(self, data):
        parsedOrder = {"id": None, "symbol": None, "price": None, "amount": None, "takerOrMaker": None, "datetime": None, "fee": None, "fee_currency": None,
                       "side": None, "timestamp": None, "status": None}
        if data != {}:
            order = data
            parsedOrder["id"] = order["order_id"]
            parsedOrder["tradeId"] = order["tradeId"]
            parsedOrder["symbol"] = self._getUserSymbol(order["symbol"])
            parsedOrder["price"] = float(order["price"]) if order["price"] != "" else None
            parsedOrder['takerOrMaker'] = "maker"  # this info is not given in the api response
            parsedOrder["amount"] = float(order["filled_amount"])
            parsedOrder["side"] = order["order_side"]
            parsedOrder["timestamp"] = int(order["ts"])  # ms epoch
            parsedOrder["datetime"] = general.ts_to_datetime(parsedOrder["timestamp"])
            parsedOrder["status"] = "closed"
            parsedOrder['fee'] = order.get("fee", None)
            parsedOrder["fee_currency"] = "quoteCurrency"  # not possible to split pair to get correct quote currency 
        return parsedOrder
    
    def _parseFetchTrades(self, orders):
        if orders["code"] != 200:
            raise Exception(orders['msg'])
        parsedTradesList = []
        for orderJson in orders["data"]:
            parsedTradesList.append(self._parseFetchOrder({'data': orderJson}))
        return parsedTradesList
    
    def _parseCancelOrder(self, order):
        if order["code"] != 200:
            raise Exception(order['msg'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        parsedOrder['id'] = order["data"]["order_id"]
        parsedOrder["orderJson"] = json.dumps(order["data"])
        return parsedOrder
    
    ## Exchange functions 
    def fetch_ticker(self, symbol):
        raise NotImplementedError("method not implemented")
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = "/uapi/v1/account/balance"
        body = {"account_type":"spot","asset_type":"BALANCE"}
        try:
            resp = self._signedRequest('POST', apiUrl, body=body)
            return self._parseBalance(resp)
        except Exception as e:
            raise e
        
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}): 
        apiUrl = "/sapi/v1/order/trades_history"
        if symbol:
            body = {
                "symbol":self._getSymbol(symbol),
            }
        try:
            resp = self._signedRequest('POST', apiUrl, body=body)
            return self._parseFetchTrades(resp)
        except Exception as e:
            raise e
    
    def create_order(self, symbol, side, amount, order_type, price=None, params={}): 
        if order_type == "limit":
            return self.create_limit_order(symbol, side, amount, price, params)
        elif order_type == "market":
            return self.create_market_order(symbol, side, amount, params)
        else: raise Exception("wrong order type, only supports market and limit")
    
    def create_market_order(self, symbol, side, amount, params={}):
        apiUrl = "/sapi/v1/order/place"
        body = {
            "symbol":self._getSymbol(symbol),
            "order_type":"market",
            "order_side":side,
            "quantity":str(amount)
        }
        try:
            body.update(params) 
            resp = self._signedRequest('POST', apiUrl, body=body)
            return self._parseCreateorder(resp)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, side, amount, price, params={}):
        apiUrl = "/sapi/v1/order/place"
        body = {
            "symbol":self._getSymbol(symbol),
            "order_type":"limit",
            "order_side":side,
            "price":str(price),
            "quantity":str(amount)
        }
        try:
            body.update(params) 
            resp = self._signedRequest('POST', apiUrl, body=body)
            return self._parseCreateorder(resp)
        except Exception as e:
            raise e
    
    def cancel_order(self, id=None, symbol=None, params={}):
        apiUrl = "/sapi/v1/order/cancel"
        body = {
            "symbol":self._getSymbol(symbol),
            "order_id":id
        }
        try:
            body.update(params) 
            resp = self._signedRequest('POST', apiUrl, body=body)
            return self._parseCancelOrder(resp)
        except Exception as e:
            raise e
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        apiUrl = "/sapi/v1/order/open_orders"
        body=None
        if symbol:
            body = {
                "symbol":self._getSymbol(symbol),
            }
        try:
            resp = self._signedRequest('POST', apiUrl, body=body)
            return self._parseOpenOrders(resp)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol = None, params={}):
        raise NotImplementedError("method not supported")