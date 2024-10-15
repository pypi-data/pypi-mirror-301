import hmac
import hashlib
import base64
import json
import time
import requests
import time
from wsgiref import headers
import requests
from datetime import datetime
from urllib.parse import urlencode
from ttxt.utils import general
from ttxt.base import baseSpotExchange
from ttxt.types import baseTypes


class coinlist(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.domain_url = "https://trade-api.coinlist.co/v1"
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "-")
    
    def _getUserSymbol(self, symbol):
        return symbol.replace("-", "/")
    
    def ts_to_datetime(self, ts):
        dt = datetime.fromtimestamp(ts)
        datetime_str = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return datetime_str

    ## Auth 
    def sign(self, method, requestPath, ts, body=None, params=None):
        # Create the prehash string by concatenating required parts
        requestPath = "/v1" + requestPath
        if body: 
            what = ts + method + requestPath + json.dumps(body, separators = (',', ':'))
        else:
            what = ts + method + requestPath
        # Decode the base64 secret
        key = base64.b64decode(self.secret)
        # Create a sha256 hmac with the secret
        h = hmac.new(key, what.encode('utf-8'), hashlib.sha256)
        # Sign the required message with the hmac and finally base64 encode the result
        signature = base64.b64encode(h.digest()).decode('utf-8')
        return signature

    def parse_params_to_str(self, params):
        params = [(key, val) for key, val in params.items()]
        params.sort(key=lambda x:x[0])
        url = "?" + urlencode(params)
        if url == '?':
            return ''
        return url
    
    def _signedRequest(self, method, request_path, queryString=None, body=None):
        ts = str(int(time.time()))
        signature = self.sign(method, request_path, ts, body)
        headers = {
            'Content-Type': 'application/json',
            'CL-ACCESS-KEY': self.key,
            'CL-ACCESS-SIG': signature,
            'CL-ACCESS-TIMESTAMP': ts
        }
        url = self.domain_url+request_path
        if method == "POST":
            try:
                response = requests.post(url, data = json.dumps(body, separators = (',', ':')), headers = headers)
                return response.json()
            except Exception as e:
                raise e
        if method == "GET":
            try:
                response = requests.get(url, headers=headers)
                return response.json()
            except Exception as e:
                raise e
        if method == "DELETE":
            try:
                response = requests.delete(url, headers=headers)
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
        if 'status' in balData and balData['status'] != 200: 
            raise Exception(balData['message'])
        for ticker, balance in balData['asset_balances'].items():
            parsedBal["free"][ticker] = str(float(balance) - float(balData['asset_holds'].get(ticker, 0)))
            parsedBal["total"][ticker] = balance
        return parsedBal
    
    def _parseCreateorder(self, order):
        if 'status' in order and order['status'] != 200: 
            raise Exception(order['message'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        if "order" in order:
            orderEle = order['order']
            parsedOrder['id'] = orderEle['order_id']
            parsedOrder['side'] = orderEle['side']
            parsedOrder['amount'] = orderEle['size']
            parsedOrder['symbol'] = orderEle['symbol']
            parsedOrder["orderJson"] = json.dumps(orderEle)
        return parsedOrder
    
    def _parseOpenOrders(self, orderjson):
        if 'status' in orderjson and orderjson['status'] != 200: 
            raise Exception(orderjson['message'])
        parsedOrderList = []    
        for order in orderjson['orders']:
            currentOrder = {}
            currentOrder['id'] = order['order_id']
            currentOrder['side'] = order['side']
            currentOrder['amount'] = order['size']
            currentOrder['price'] = order.get("price", None) # market order has no price
            currentOrder['status'] = order['status']
            currentOrder["timestamps"] = order["epoch_timestamp"]
            currentOrder["orderJson"] = json.dumps(order)
            parsedOrderList.append(currentOrder)
        return parsedOrderList
    
    def _parseFetchOrder(self, data):
        parsedOrder = {"id": None, "symbol": None, "price": None, "amount": None, "takerOrMaker": None, "datetime": None, "fee": None, "fee_currency": None,
                       "side": None, "timestamp": None, "status": None}
        if 'status' in data and data['status'] != 200: 
            raise Exception(data['message'])
        order = data
        parsedOrder["id"] = order["order_id"]
        parsedOrder["symbol"] = order["symbol"]
        if "price" in order:
            parsedOrder["price"] = float(order["price"])
        else:
            parsedOrder["price"] = None
        parsedOrder["amount"] = float(order["size"])
        parsedOrder["side"] = order["side"]
        parsedOrder["timestamp"] = order["epoch_timestamp"]
        return parsedOrder
    
    def _parseFetchTrades(self, orderjson):
        if 'status' in orderjson and orderjson['status'] != 200: 
            raise Exception(orderjson['message'])
        parsedTradesList = []
        if "fills" in orderjson:
            for order in orderjson["fills"]:
                currentTrade = {}
                currentTrade["tradeId"] = order["order_id"]  # trade Id not provided
                currentTrade["id"] = order["order_id"]
                currentTrade["side"] = "buy" if float(order["quantity"]) > 0 else "sell"  # negative quantity for sell
                currentTrade["amount"] = order["quantity"]
                currentTrade["price"] = order.get("price", None)
                currentTrade["timestamp"] = general.datetime_to_ts_ms(order['logical_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
                currentTrade["datetime"] = general.ts_to_datetime(currentTrade["timestamp"])
                currentTrade['takerOrMaker'] = order["fee_type"]
                currentTrade['fee'] = order["fee"]
                currentTrade["fee_currency"] = order["fee_currency"]
                parsedTradesList.append(currentTrade)
        return parsedTradesList
    
    def _parseCancelorder(self, order, id): # doesnt return any response?
        if 'status' in order and order['status'] != 200: 
            raise Exception(order['message'])
        parsedOrder = {'id': id, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        return parsedOrder
    
    ## Exchange functions 
    def fetch_ticker(self, symbol):
        raise NotImplementedError("method not implemented")
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = "/balances"
        try:
            resp = self._signedRequest('GET', apiUrl)
            return self._parseBalance(resp)
        except Exception as e:
            raise e
        
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}): 
        apiUrl = "/fills"
        try:
            params['count'] = 500 # set to max
            # if symbol:
            #     params["symbol"] = self._getSymbol(symbol)
            # if since:
            #     params["start_time"] = self.ts_to_datetime(int(since))
            # if 'endTime' in params and params['endTime']:
            #     params['end_time'] = self.ts_to_datetime(int(params['endTime']))
            # if limit:
            #     params['limit'] = int(limit)
            ## params not used
            response = self._signedRequest('GET', request_path=apiUrl, queryString=params)
            return self._parseFetchTrades(response)
        except Exception as e:
            raise e
    
    def create_order(self, symbol, side, amount, order_type, price=None, params={}): 
        try:
            if order_type == "market":
                self.create_market_order(symbol, amount, side, params={})
            elif order_type == "limit":
                self.create_limit_order(symbol, amount, side, price, params={})
        except Exception as e:
            raise e
    
    def create_market_order(self, symbol, side, amount, params={}):
        apiUrl = "/orders"
        body = {
            "symbol":self._getSymbol(symbol),
            "type":"market",
            "side":side,
            "size":str(amount)
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body)
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, side, amount, price, params={}):
        apiUrl = "/orders"
        body = {
            "symbol":self._getSymbol(symbol),
            "type":"limit",
            "side":side,
            "size":str(amount),
            "price":str(price),
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body)
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def cancel_order(self, id=None, symbol=None, params={}):
        apiUrl = f"/orders/{id}"
        try:
            response = self._signedRequest('DELETE', request_path=apiUrl)
            return self._parseCancelorder(response, id)
        except Exception as e:
            raise e
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        apiUrl = "/orders"
        try:
            response = self._signedRequest('GET', request_path=apiUrl)
            return self._parseOpenOrders(response)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol = None, params={}):
        apiUrl = f"/orders/{id}"
        try:
            response = self._signedRequest('GET', request_path=apiUrl)
            return self._parseFetchOrder(response)
        except Exception as e:
            raise e