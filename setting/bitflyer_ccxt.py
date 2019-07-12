# -*- coding: utf-8 -*-
import sys
import os
import random
import ccxt

#### api keys #####
api_keys = [
    {"api_key": "Csb6JiQsgU4chB5P3n8Bkz", "api_secret": "JBQT3MDVMkhnBiAbDIMNKdsvDLa4SIFu6ghspNGyFP4="},
    {"api_key": "Bc1MKLZx5UtPpAePaUxWwC", "api_secret": "NHGsAyxWg3qw89B7ud9YnrqoN8eCPteBhtW9FfvRPBo="},
    {"api_key": "YBghKFpXpArY2AWTsTZ92n", "api_secret": "2GEuAGJSw1mvnVy6R9PhpVC/G/msL59O5FKV99U6qV4="},
    {"api_key": "UfL8GqtffiA4NDk2y18qqA", "api_secret": "LJbgCgnPdd8vIRwUWYDihFkKxLe7m8CUmOg6TtrN/ig="},
    {"api_key": "MX7bJS7WxanpCGpjdSkjZr", "api_secret": "6W4iI8fiKTe1+YSIEaj4DN/O4B7vP5dNUGpHtpJj2S0="}
]

num = random.randint(0,4)
using_key = api_keys[num]

API_KEY = using_key["api_key"]
API_SECRET = using_key["api_secret"]

##### set ccxt #####
bitflyer = ccxt.bitflyer({
    "apiKey" : API_KEY,
    "secret" : API_SECRET
})


