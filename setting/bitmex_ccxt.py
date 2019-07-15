# -*- coding: utf-8 -*-
import sys
import os
import random
import ccxt

#### api keys #####
api_keys = [
    {"api_key": "dQmfJ2YDzz3Gv9Gcd7UmbIWf", "api_secret": "Wm6wLox59tHr9tkvbSyjJ3zsgb3nQ3sObhXBqqiV77XpV7CA"},
    {"api_key": "afuglKp2PIjbWabzwB9VCU_a", "api_secret": "CyjUIS4u7ci8xZILPxnXit7FpyaZGQcJ92WNaKr40qsnszEG"},
    {"api_key": "zztLy9dWIWWq9tb93kkBMPXB", "api_secret": "_hVyuWlOYoKhC9J8llDONRhQUhdQzjdUMHiH3qxKYUze2aoW"},
    {"api_key": "bF7qRbmtU21WuHTvHhF67iRt", "api_secret": "HQnkR4651vq0QvDGd8edMfYOCV8urj3XnSu4eza8dwYDNWtM"},
    {"api_key": "jpPdfjooxtbSdS2Z-iNsRb89", "api_secret": "ek3kEdwjP3iEbf51qHPnUxLR5A_7u06Ji2_5CJyv2ha2a63T"}
]

num = random.randint(0,4)
using_key = api_keys[num]

API_KEY = using_key["api_key"]
API_SECRET = using_key["api_secret"]

##### set ccxt #####
bitmex = ccxt.bitmex({
    "apiKey" : API_KEY,
    "secret" : API_SECRET
})


