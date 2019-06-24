# -*- coding: utf-8 -*-
import sys
import os
import random
import ccxt

#### api keys #####
api_keys = [
    {"api_key": "P80YN-QI1UVhVk76", "api_secret": "Th2T19fx7oe6yi45OpQesJSyR49CrKVQ"},
    {"api_key": "P80YN-QI1UVhVk76", "api_secret": "Th2T19fx7oe6yi45OpQesJSyR49CrKVQ"},
    {"api_key": "P80YN-QI1UVhVk76", "api_secret": "Th2T19fx7oe6yi45OpQesJSyR49CrKVQ"},
    {"api_key": "P80YN-QI1UVhVk76", "api_secret": "Th2T19fx7oe6yi45OpQesJSyR49CrKVQ"},
    {"api_key": "P80YN-QI1UVhVk76", "api_secret": "Th2T19fx7oe6yi45OpQesJSyR49CrKVQ"}
]

num = random.randint(0,4)
using_key = api_keys[num]

API_KEY = using_key["api_key"]
API_SECRET = using_key["api_secret"]

##### set ccxt #####
coincheck = ccxt.coincheck({
    "apiKey" : API_KEY,
    "secret" : API_SECRET
})

