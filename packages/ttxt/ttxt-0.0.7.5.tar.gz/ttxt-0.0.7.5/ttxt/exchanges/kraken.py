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



class kraken(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.domain_url = "https://api.kraken.com"
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "")
    
    def _getUserSymbol(self, symbol):
        raise NotImplementedError("method not implemented")
    
    ## Auth 
    def get_kraken_signature(self, urlpath, data):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def kraken_request(self, uri_path, data={}):
        data.update({"nonce": str(int(1000*time.time()))})
        headers = {}
        headers['API-Key'] = self.key
        # get_kraken_signature() as defined in the 'Authentication' section
        headers['API-Sign'] = self.get_kraken_signature(uri_path, data)
        req = requests.post((self.domain_url + uri_path), headers=headers, data=data)
        return req
        
    def _signedRequest(self, method, request_path, queryString, body):
        if method == "POST":
            try:
                response = self.kraken_request(request_path, body)
                return response.json()
            except Exception as e:
                raise e
        if method == "GET":
            try:
                response = self.kraken_request(request_path, queryString)
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
        if "error" in balData and len(balData["error"]) > 0: 
            raise Exception(balData['error'][0])
        data = balData.get("result", None)
        if data is not None:
            for element, value in data.items():
                parsedBal["free"][element] =  str(float(value['balance']) - float(value["hold_trade"]))
                parsedBal["total"][element] = value['balance']
        return parsedBal
    
    def _parseCreateorder(self, order):
        if "error" in order and len(order["error"]) > 0: 
            raise Exception(order['error'][0])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        if "result" in order and order["result"] != {}:
            parsedOrder['id'] = order['result']['txid'][0]
            parsedOrder["orderJson"] = json.dumps(order)
        return parsedOrder
    
    def _parseOpenOrders(self, orders):
        if "error" in orders and len(orders["error"]) > 0: 
            raise Exception(orders['error'][0])
        parsedOrderList = []    
        if "result" in orders and orders['result'] != {}:
            for orderId, orderJson in orders["result"]["open"].items():
                currentOrder = {} 
                currentOrder["id"] = orderId
                currentOrder["symbol"] = orderJson["descr"]["pair"]
                currentOrder["price"] = float(orderJson["descr"]["price"])
                currentOrder["amount"] = float(orderJson["vol"])
                currentOrder["side"] = orderJson["descr"]["type"]
                currentOrder["timestamp"] = orderJson["opentm"]
                currentOrder["status"] = "open"
                currentOrder["orderJson"] = json.dumps(orderJson)
                parsedOrderList.append(currentOrder)
        return parsedOrderList
    
    def _parseFetchOrder(self, data):
        parsedOrder = {"id": None, "symbol": None, "price": None, "amount": None, "takerOrMaker": None, "datetime": None, "fee": None, "fee_currency": None,
                       "side": None, "timestamp": None, "status": None}
        if "data" in data and data["data"] != {}:
            order = data['data']
            if type(order) == list:
                order = order[0]
            parsedOrder["id"] = order["ordertxid"]
            parsedOrder["tradeId"] = order["trade_id"]
            parsedOrder["symbol"] = order["pair"]
            if "price" in order:
                parsedOrder["price"] = float(order["price"])
            else:
                parsedOrder["price"] = float(order["priceAvg"])  # check this
            parsedOrder['takerOrMaker'] = "maker" if order["maker"] == True else "taker"
            parsedOrder["amount"] = float(order["vol"])
            parsedOrder["side"] = order["type"]
            parsedOrder["timestamp"] = int(order["time"]*1000)  # ms epoch
            parsedOrder["datetime"] = general.ts_to_datetime(parsedOrder["timestamp"])
            parsedOrder["status"] = "closed"
            parsedOrder['fee'] = order.get("fee", None)
            parsedOrder["fee_currency"] = "quoteCurrency"  # not possible to split pair to get correct quote currency 
        return parsedOrder
    
    def _parseFetchTrades(self, orders):
        if "error" in orders and len(orders["error"]) > 0: 
            raise Exception(orders['error'][0])
        parsedTradesList = []
        for someId, orderJson in orders["result"]["trades"].items():
            parsedTradesList.append(self._parseFetchOrder({'data': orderJson}))
        return parsedTradesList
    
    def _parseCancelOrder(self, order, id):
        if "error" in order and len(order["error"]) > 0: 
            raise Exception(order['error'][0])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        parsedOrder['id'] = id
        parsedOrder["orderJson"] = json.dumps(order["result"])
        return parsedOrder
    
    ## Exchange functions 
    def fetch_ticker(self, symbol):
        raise NotImplementedError("method not implemented")
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = "/0/private/BalanceEx"
        try:
            resp = self._signedRequest('GET', apiUrl, params, '')
            return self._parseBalance(resp)
        except Exception as e:
            raise e
        
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}): 
        apiUrl = "/0/private/TradesHistory"
        try:
            params = {
                "type": "all",
                "trades": False,
                "consolidate_taker": True
            }
            if since:
                params["start"] = int(since)
            if 'endTime' in params and params['endTime']:
                params['end'] = int(since)
            response = self._signedRequest('POST', request_path=apiUrl, queryString='', body=params)
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
        apiUrl = "/0/private/AddOrder"
        body = {
            "ordertype": "market",
            "type": side,
            "volume": str(amount),
            "pair": self._getSymbol(symbol)
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body, queryString='')
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, side, amount, price, params={}):
        apiUrl = "/0/private/AddOrder"
        body = {
            "ordertype": "limit",
            "type": side,
            "volume": str(amount),
            "pair": self._getSymbol(symbol),
            "price": str(price)
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, queryString='', body=body)
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def cancel_order(self, id=None, symbol=None, params={}):
        apiUrl = "/0/private/CancelOrder"
        ticker = self._getSymbol(symbol)
        try:
            params={}
            if id is not None:
                params['txid'] = id
            if symbol is not None:
                params['pair'] = self._getSymbol(ticker)
            params.update(params)
            response = self._signedRequest('POST', request_path=apiUrl, queryString='',body=params)
            return self._parseCancelOrder(response, id)
        except Exception as e:
            raise e
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        apiUrl = "/0/private/OpenOrders"
        try:
            response = self._signedRequest('POST', request_path=apiUrl, queryString=[], body={})
            return self._parseOpenOrders(response)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol = None, params={}):
        raise NotImplementedError("method not supported")