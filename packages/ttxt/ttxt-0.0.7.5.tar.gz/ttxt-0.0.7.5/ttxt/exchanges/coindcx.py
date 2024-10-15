import hmac
import hashlib
import base64
import json
import time
import requests
import time
from wsgiref import headers
import requests
from urllib.parse import urlencode
from ttxt.utils import general
from ttxt.base import baseSpotExchange
from ttxt.types import baseTypes


class coindcx(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.domain_url = "https://api.coindcx.com"
        self.success_sode = '00000'
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "")
    
    def _getUserSymbol(self, symbol):
        raise NotImplementedError("method not implemented")
    
    ## Auth 
    def sign(self, body):
        # python3
        secret_bytes = bytes(self.secret, encoding='utf-8')
        # Generating a timestamp.
        body.update({"timestamp": self.generate_timestamp()})
        json_body = json.dumps(body, separators = (',', ':'))
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        return signature, json_body

    def parse_params_to_str(self, params):
        params = [(key, val) for key, val in params.items()]
        params.sort(key=lambda x:x[0])
        url = "?" + urlencode(params)
        if url == '?':
            return ''
        return url
    
    def generate_timestamp(self):
        return int(round(time.time() * 1000))
    
    def _signedRequest(self, method, request_path, queryString, body):
        signature, json_body = self.sign(body)
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        if method == "POST":
            url = self.domain_url+request_path
            try:
                response = requests.post(url, data = json_body, headers = headers)
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
        if 'code' in balData: 
            raise Exception(balData['message'])
        for element in balData:
            parsedBal["free"][element["currency"]] = element["balance"]
            parsedBal["total"][element["currency"]] = str(float(element['balance'])+float(element['locked_balance']))
        return parsedBal
    
    def _parseCreateorder(self, order):
        if 'code' in order: 
            raise Exception(order['message'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        if "orders" in order and order["orders"] != []:
            order = order["orders"][0]
            parsedOrder['id'] = order['id']
            parsedOrder['side'] = order['side']
            parsedOrder['amount'] = order['total_quantity']
            parsedOrder['price'] = order.get("price_per_unit", None) # market order has no price
            parsedOrder["orderJson"] = json.dumps(order)
        return parsedOrder
    
    def _parseOpenOrders(self, orderjson):
        if 'code' in orderjson: 
            raise Exception(orderjson['message'])
        parsedOrderList = []    
        for order in orderjson['orders']:
            currentOrder = {}
            currentOrder['id'] = order['id']
            currentOrder['side'] = order['side']
            currentOrder['amount'] = order['total_quantity']
            currentOrder['price'] = order.get("price_per_unit", None) # market order has no price
            currentOrder['status'] = order['status']
            currentOrder["timestamps"] = general.datetime_to_ts_ms(order["created_at"], format='%Y-%m-%dT%H:%M:%S.%fZ')
            currentOrder["orderJson"] = json.dumps(order)
            parsedOrderList.append(currentOrder)
        return parsedOrderList
    
    def _parseFetchOrder(self, data):
        parsedOrder = {"id": None, "symbol": None, "price": None, "amount": None, "takerOrMaker": None, "datetime": None, "fee": None, "fee_currency": None,
                       "side": None, "timestamp": None, "status": None}
        if 'code' in data: 
            raise Exception(data['message'])
        order = data
        if type(order) == list:
            order = order[0]
        parsedOrder["id"] = order["id"]
        parsedOrder["symbol"] = order["market"]
        if "price" in order:
            parsedOrder["price"] = float(order["price_per_unit"])
        else:
            parsedOrder["price"] = float(order["avg_price"])
        parsedOrder["amount"] = float(order["total_quantity"])
        parsedOrder["side"] = order["side"]
        parsedOrder["timestamp"] = int(order["created_at"])
        parsedOrder["datetime"] = general.ts_to_datetime(parsedOrder["timestamp"])
        parsedOrder["status"] = order.get('status', None)
        parsedOrder['fee'] = order.get('fee_amount', None)
        return parsedOrder
    
    def _parseFetchTrades(self, orderjson):
        if 'code' in orderjson: 
            raise Exception(orderjson['message'])
        parsedTradesList = []
        for order in orderjson:
            currentTrade = {}
            currentTrade["tradeId"] = order["id"]
            currentTrade["id"] = order["order_id"]
            currentTrade["side"] = order["side"]
            currentTrade["amount"] = order["quantity"]
            currentTrade["price"] = order.get("price", None)
            currentTrade["timestamp"] = float(order["timestamp"])
            currentTrade["datetime"] = general.ts_to_datetime(currentTrade["timestamp"])
            currentTrade['takerOrMaker'] = "maker" # coindcx doesnt provide this info
            currentTrade['fee'] = order["fee_amount"]
            currentTrade["fee_currency"] = "quoteCurrency"  # api doesnt return this in response
            parsedTradesList.append(currentTrade)
        return parsedTradesList
    
    def _parseCancelorder(self, order, id): # doesnt return any response?
        if 'code' in order and order['code'] != 200: 
            raise Exception(order['message'])
        parsedOrder = {'id': id, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        return parsedOrder
    
    ## Exchange functions 
    def fetch_ticker(self, symbol):
        raise NotImplementedError("method not implemented")
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = "/exchange/v1/users/balances"
        try:
            resp = self._signedRequest('POST', apiUrl, params, {})
            return self._parseBalance(resp)
        except Exception as e:
            raise e
        
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}): 
        apiUrl = "/exchange/v1/orders/trade_history"
        try:
            body = {
                "symbol": self._getSymbol(symbol),
                "limit": 5000 # set to max
            }
            if symbol:
                body["symbol"] = self._getSymbol(symbol)
            if since:
                body["from_timestamp"] = int(since)
            if 'endTime' in params and params['endTime']:
                params['to_timestamp'] = int(params['endTime'])
            if limit:
                params['limit'] = int(limit)
            response = self._signedRequest('POST', request_path=apiUrl, queryString='', body=body)
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
        apiUrl = "/exchange/v1/orders/create"
        body = {
            "side": side,    #Toggle between 'buy' or 'sell'.
            "order_type": "market_order", #Toggle between a 'market_order' or 'limit_order'.
            "market": self._getSymbol(symbol), #Replace 'SNTBTC' with your desired market pair.
            "total_quantity": float(amount), #Replace this with the quantity you want
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body, queryString='')
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, side, amount, price, params={}):
        apiUrl = "/exchange/v1/orders/create"
        body = {
            "side": side,    #Toggle between 'buy' or 'sell'.
            "order_type": "limit_order", #Toggle between a 'market_order' or 'limit_order'.
            "market": self._getSymbol(symbol), #Replace 'SNTBTC' with your desired market pair.
            "price_per_unit": float(price), #This parameter is only required for a 'limit_order'
            "total_quantity": float(amount), #Replace this with the quantity you want
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body, queryString='')
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def cancel_order(self, id=None, symbol=None, params={}):
        apiUrl = "/exchange/v1/orders/cancel"
        try:
            body = {
                "id": id,
            }
            body.update(params)
            response = self._signedRequest('POST', request_path=apiUrl, queryString='',body=body)
            return self._parseCancelorder(response, id)
        except Exception as e:
            raise e
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        apiUrl = "/exchange/v1/orders/active_orders"
        ticker = self._getSymbol(symbol)
        try:
            body = {
                "market": ticker
            }
            response = self._signedRequest('POST', request_path=apiUrl, queryString='', body=body)
            return self._parseOpenOrders(response)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol = None, params={}):
        apiUrl = "/exchange/v1/orders/status"
        try:
            body = {
                "id": id
            }
            body.update(params)
            response = self._signedRequest('POST', request_path=apiUrl, queryString='', body=body)
            return self._parseFetchOrder(response)
        except Exception as e:
            raise e