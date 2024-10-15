from ttxt.base import baseFuturesExchange, baseSpotExchange
from ttxt.exchanges.ascendex import ascendex
from ttxt.exchanges.gateFutures import gateFutures
from ttxt.exchanges.bybitFutures import bybitFutures
from ttxt.exchanges.bitgetFutures import bitgetFutures
from ttxt.exchanges.bingx import bingx
from ttxt.exchanges.biconomy import biconomy
from ttxt.exchanges.mexc import mexc
from ttxt.exchanges.gateio import gateio
from ttxt.exchanges.bybit import bybit
from ttxt.exchanges.okx import okx
from ttxt.exchanges.huobi import huobi
from ttxt.exchanges.bitmart import bitmart
from ttxt.exchanges.cryptocom import cryptocom
from ttxt.exchanges.bitget import bitget
from ttxt.exchanges.binance import binance
from ttxt.exchanges.kucoin import kucoin
from ttxt.exchanges.kraken import kraken
from ttxt.exchanges.blofin import blofin
from ttxt.exchanges.coindcx import coindcx
from ttxt.exchanges.coinlist import coinlist
from ttxt.exchanges.coinstore import coinstore
from ttxt.exchanges.coinbase import coinbase
from ttxt.exchanges.whitebit import whitebit

exchanges = [
    "ascendex",
    "biconomy",
    "binance",
    "bingx",
    "bitgetFutures",
    "bitget",
    "bybitFutures",
    "gateFutures",
    "kucoin"
    "mexc",
    "gateio",
    "bybit",
    "okx",
    "huobi",
    "bitmart",
    "cryptocom",
    "kraken",
    "blofin",
    "coindcx",
    "coinlist",
    "coinstore",
    "coinbase",
    "whitebit"
]

base = [
    "baseFuturesExchange",
    "baseSpotExchange"
]

_all__ =  exchanges + base