#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 15:24:07 2021

@author: alexanderel-hajj
"""

length = len([v for k,v in data.items() if k=='messages'][0])
embedded_data = [v for k,v in data.items() if k=='messages'][0]
dataAll = []
for i in range(0,length):
    embeds = embedded_data[i][0]['embeds'][0]['title']
    timestamp = embedded_data[i][0]['timestamp']
    if embeds.split()[0] in ('BTO', 'STC'):
        date_formatted = embeds.split()[3].split('/')
        if len(date_formatted[0]) == 1:
            month = '0' + date_formatted[0]
        if len(date_formatted[1]) == 1:
            day = '0' + date_formatted[1]
        date_expiry = '2021' + month + day
        if embeds.split()[0] == 'BTO':
            action = 'BUY'
        else:
            action = 'SELL'
        tmp = {'Action Symbol': embeds.split()[0], 
               'Action': action,
               'Ticker': embeds.split()[1], 
               'Strike Price': embeds.split()[2][:-1], 
               'Call Or Put': embeds.split()[2][-1:],
               'Expiry Date': date_expiry,
               'Other': [x.lower().replace("=", "")  for x in embeds.split()[4:]]}
        
        if 'entry' in tmp['Other']:
            if tmp['Other'][1][0] == '.':
                tmp['Limit Price'] = '0' + tmp['Other'][1]
            else:
                tmp['Limit Price'] = tmp['Other'][1]
        
        dataAll.append(tmp)
    else:
        """
        For later purposes, we will do something with cases not starting in BTO/STC
        if tmp['Embeds'].split()[0] not in ('BTO', 'STC'):
            tmp['Format'] = 0
        """
        pass

