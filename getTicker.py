#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:30:42 2021

@author: alexanderel-hajj
"""



import json
from os.path import join

data_path = "./cached/"
server_name = "814189734884409364_Rags To Riches Trading/"

"""
STC = Sell To Close
JD = ticker
79C = Call option at strike price of $79
7/2 = expiry of the option is on July 2nd
two options for the first one, BTO (buy) STC (sell), 
unless the guy writes calls too which i highly doubt
then for 79C it can also be 79P which is a put
"""

room1 = '817816874993451038_🚨︱moneybags-daytrades' 
room2 = '838942842000637992_🚨︱stonk-king-options'
room3 = '844627582074093598_🚨︱rich-penny-swings'


path1 = data_path + server_name + room2

with open(join(path1, "2021_6_29.cache.json"), "r") as j:
    data=json.load(j)


dataAll = []
for k,v in data.items():
    if k == 'messages':
        length = len(v)
        print(length)
        for i in range(0,length):
            embeds = v[i][0]['embeds'][0]['title']
            timestamp = v[i][0]['timestamp']

            tmp = {"Embeds": embeds, "Timestamp": timestamp}
            
            if tmp['Embeds'].split()[0] in ('BTO', 'STC'):
                tmp['Format'] = 1
                tmp['Action'] = tmp['Embeds'].split()[0]
                tmp['Ticker'] = tmp['Embeds'].split()[1]
                tmp['Strike price'] = tmp['Embeds'].split()[2]
                if tmp['Strike price'][-1:] == 'P':
                    tmp['Call/Put'] = 'Put'
                elif tmp['Strike price'][-1:] == 'C':
                    tmp['Call/Put'] = 'Call'
                tmp['Expiry date'] = tmp['Embeds'].split()[3]  
                tmp['Other'] = tmp['Embeds'].split()[4:]
            if tmp['Embeds'].split()[0] not in ('BTO', 'STC'):
                tmp['Format'] = 0

            dataAll.append(tmp)
        

