# -*- coding: utf-8 -*-
import sys
import os
import random
import ccxt

#### api keys #####
api_keys = [
    {"api_key": "P80YN-QI1UVhVk76", "api_secret": "Th2T19fx7oe6yi45OpQesJSyR49CrKVQ"},
    {"api_key": "4hyuNHWFuH66vDGY", "api_secret": "qahvbs54s-_49ulTclE7Y77NKHNPwiKa"},
    {"api_key": "8lsM6sY0fcU1ExFg", "api_secret": "BBULQSREkwQldi4YmCpCepzrSeQWCoxp"},
    {"api_key": "0bPwCLosj68KSL9d", "api_secret": "Q7K5xhre5Mrq5h70khFBWuIVjhJ_YbbD"},
    {"api_key": "IvFhWpIWtO0rLDtq", "api_secret": "yNHXu3BEepJfD50nn2z9E7NwkFO-nR0N"}
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

