import hmac
import base64
import hashlib
import json
import time
import requests
from datetime import datetime as dt
from ttxt.base import baseSpotExchange
from ttxt.types import baseTypes
from ttxt.utils import general

'''
kwargs = {}
'''
class whitebit(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.domain_url = "https://whitebit.com"

    def _getSymbol(self, symbol):
        return symbol.replace("/", "_")

    ## Auth 
    def get_expire(self):
        return int((time.time() + 1) * 1000)  # websockets use seconds
    
    def generate_timestamp(self):
        """
        Return a millisecond integer timestamp.
        """
        return int(time.time() * 10**3)
    
    def _get_sign(self, payload):
        # payload = ":"+ payload + "&secret_key=" + self.secret
        payload = payload + "&secret_key=" + self.secret
        signature = hashlib.md5(payload.encode()).hexdigest().upper()
        return signature
        
    def _parseParams(self, paramsMap):
        sortedKeys = sorted(paramsMap)
        paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
        # return paramsStr+"&timestamp="+str(int(time.time() * 1000))
        return paramsStr
    
    def _check_resp_status(self, resp):
        if "code" in resp:
            if resp["code"] != 0:
                raise Exception(resp["msg"])
            else:
                return resp  # success 
        if "message" in resp:
            raise Exception(resp["message"])
        return resp
    
    def _authenticate(self,data_json):
        payload = base64.b64encode(data_json.encode('ascii'))
        signature = hmac.new(self.secret.encode('ascii'), payload, hashlib.sha512).hexdigest()
        headers = {
            'Content-type': 'application/json',
            'X-TXC-APIKEY': self.key,
            'X-TXC-PAYLOAD': payload,
            'X-TXC-SIGNATURE': signature,
        }
        return headers
        
    def _send_request(self, method, payload={}):
        payload.update({
            'nonce': time.time_ns() // 1_000_000,
            'nonceWindow': True 
        })
        data_json = json.dumps(payload, separators=(',', ':'))  # use separators param for deleting spaces
        headers = self._authenticate(data_json)
        try:
            completeUrl = self.domain_url + payload['request']
            headers.update({'Content-Type': 'application/json'})
            if method == "GET":
                response = requests.get(completeUrl, headers=headers)
                return response.json()
            if method == "POST":
                response = requests.post(completeUrl, headers=headers, data=data_json)
                return response.json()
            if method == "DELETE":
                response = requests.delete(completeUrl, headers=headers, data=data_json)
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
        
    def _prepare_params(self, params):
        payload = "&".join(
                [
                    str(k) + "=" + str(v)
                    for k, v in params.items()  #use for sort: sorted(params.items())
                    if v is not None
                ]
            )
        return payload

    ## parsers
    def _parseCreateorder(self, order):
        if 'errors' in order:
            if not order['errors'] == {}:
                raise Exception(order['errors'])
            elif not order['message'] == {}:
                raise Exception(order['message'])
        parsedOrder = {}
        parsedOrder["id"] = order.get('orderId', None)
        parsedOrder["symbol"] = order.get('symbol', None)
        parsedOrder["price"] = order.get("price", None)
        parsedOrder["amount"] = order.get("origQty", None)
        if "side" in order: 
            parsedOrder["side"] = order["side"].lower()
        else:
            parsedOrder["side"] = None
        parsedOrder["timestamp"] = order.get("transactTime", None)
        parsedOrder["status"] = "closed"
        parsedOrder["orderJson"] = json.dumps(order)
        return parsedOrder

    def _parseBalance(self, balanceData):
        if 'errors' in balanceData:
            if not balanceData['errors'] == {}:
                raise Exception(balanceData['errors'])
            elif not balanceData['message'] == {}:
                raise Exception(balanceData['message'])
        parsedBal = {"free": {}, "total": {}}
        for token in balanceData:
            parsedBal["free"][token] = float(balanceData[token]["available"])
            parsedBal["total"][token] = parsedBal["free"][token] + float(balanceData[token]["freeze"])
        return parsedBal

    def _parseOpenOrders(self, orders):
        if 'errors' in orders:
            if not orders['errors'] == {}:
                raise Exception(orders['errors'])
            elif not orders['message'] == {}:
                raise Exception(orders['message'])
        parsedOrderList = []
        for order in orders:
            parsedOrderList.append(self._parseCreateorder(order))
        return parsedOrderList
    
    def _parseTrades(self, trades):
        if 'errors' in trades:
            if not trades['errors'] == {}:
                raise Exception(trades['errors'])
            elif not trades['message'] == {}:
                raise Exception(trades['message'])
        def parseTrade(trade):
            parsedTrade = {}
            parsedTrade["symbol"] = trade.get("symbol", None)
            parsedTrade["id"] = trade.get("id", None)
            parsedTrade["tradeId"] = trade.get("id", None)
            parsedTrade["side"] = trade["side"]
            parsedTrade["price"] = trade.get("price", None)
            parsedTrade["amount"] = trade.get("qty", None)
            parsedTrade["takerOrMaker"] = "maker" if trade["role"]==1 else "taker"
            if "time" in trade:
                parsedTrade["timestamp"] = int(float(trade["time"]))
                parsedTrade["datetime"] = general.ts_to_datetime(parsedTrade["timestamp"])
            else: 
                parsedTrade["timestamp"] = None
                parsedTrade["datetime"] = None
            parsedTrade["feeCurrency"] = "quoteCurrency"
            parsedTrade["fee"] = float(trade["fee"])
            return parsedTrade
        parsedTradeList = []
        for trade in trades:
            parsedTradeList.append(parseTrade(trade))
        return parsedTradeList

    ## Exchange functions
    # buy orders size are in quote and sell orders are in base
    def create_market_order(self, symbol, side, amount, params={}, price=None):
        params = {
            "request": '/api/v4/order/market',
            "market": self._getSymbol(symbol),
            "side": side,
            "amount":amount
        }
        try:
            resp = self._send_request(method='POST', payload=params)
            return self._parseCreateorder(resp)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, side, amount, price, params={}):
        params = {
            "request": '/api/v4/order/new',
            "market": self._getSymbol(symbol),
            "side": side,
            "amount":amount,
            "price": price
        }
        try:
            resp = self._send_request(method='POST', payload=params)
            return self._parseCreateorder(resp)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol=None):
        raise NotImplementedError("method not implemented")
    
    def fetch_open_orders(self, symbol=None,  kwargs=None):
        params = {
            "request": '/api/v4/orders',
            "market": self._getSymbol(symbol)
        }
        try:
            resp = self._send_request(method='POST', payload=params)
            return self._parseOpenOrders(resp)
        except Exception as e:
            raise e
        
    def cancel_order(self, id, symbol):
        params = {
            "request": '/api/v4/order/cancel',
            "market": self._getSymbol(symbol),
            "orderId": id
        }
        try:
            resp = self._send_request(method='POST', payload=params)
            return self._parseCreateorder(resp)
        except Exception as e:
            raise e
        
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        params = {"request": '/api/v4/trade-account/balance'}
        try:
            resp = self._send_request(method='POST', payload=params)
            return self._parseBalance(resp)
        except Exception as e:
            raise e
    
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        params = {
            "request": '/api/v4/trade-account/executed-history',
            "market": self._getSymbol(symbol)
        }
        if limit:
            params['limit'] = limit
        try:
            resp = self._send_request(method='POST', payload=params)
            return self._parseTrades(resp)
        except Exception as e:
            raise e
    
    def fetch_ticker(self, symbol: str, params={}) -> baseTypes.Ticker:
        raise NotImplementedError("method not implemented")

    def fetch_order_book(self, symbol: str, limit=None, params={}) -> baseTypes.OrderBook:
        raise NotImplementedError("method not implemented")