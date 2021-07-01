#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:30:42 2021

@author: alexanderel-hajj
"""



import json
import os.path
from os import path
from os.path import join
from datetime import datetime, timedelta

import configparser



"""
STC = Sell To Close
JD = ticker
79C = Call option at strike price of $79
7/2 = expiry of the option is on July 2nd
two options for the first one, BTO (buy) STC (sell), 
unless the guy writes calls too which i highly doubt
then for 79C it can also be 79P which is a put
"""

data_path = "./cached/"
server_name = "814189734884409364_Rags To Riches Trading/"
room1 = '817816874993451038_🚨︱moneybags-daytrades' 
room2 = '838942842000637992_🚨︱stonk-king-options'
room3 = '844627582074093598_🚨︱rich-penny-swings'

todays_date = str(datetime.today())[:19].replace(' ', '-')

def check_date(data_path, server_name, room, use_old = False):
    """
    Check if there was a post today
    """
    todays_date_str = str(datetime.today())
    todays_date = datetime.today()
    
    if use_old:
        days = timedelta(1)
        new_date = str(todays_date - days)
        print("Todays date subtracted by three days: {}".format(new_date))
    
        if new_date[5] == '0':
            month = new_date[6]
        else:
            month = new_date[5:7]
        if new_date[8] == '0':
            day = new_date[9]
        else:
            day = new_date[8:10]
        todays_date_new = new_date[0:4] + '_' + month + '_' + day
    else:
        if todays_date_str[5] == '0':
            month = todays_date_str[6]
        else:
            month = todays_date_str[5:7]
        if todays_date_str[8] == '0':
            day = todays_date_str[9]
        else:
            day = todays_date_str[8:10]
        todays_date_new = todays_date_str[0:4] + '_' + month + '_' + day

    filename = todays_date_new + '.cache.json'
    
    filepath = data_path + server_name + room + '/' + filename
    
    file_exists = path.exists(filepath)
    
    return file_exists, filepath

file_exists, filepath = check_date(data_path, server_name, room2, use_old = True)


if file_exists is True:
    print("Post was made today!, Can import today's data")
    with open(filepath, "r") as j:
        data=json.load(j)
else:
    """
    Option to use yesterday's post?
    """
    pass



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



"""
Which order to go through with?
Latest one for now
"""
def get_most_current_order(data):
    """ Gets most current order
    """
    bad_words = ['trim', 'closing', 'trimming', 'selling', 'all out', 'sold']
    good_words = 'entry'
    count=0
    for idx,lst in enumerate(data):
        if good_words in lst['Other']:
            current_order = data[idx]
            count+=1
            if count == 1:
                return current_order
            
curr=get_most_current_order(dataAll)

"""
Write order to .ini file
"""

write_config = configparser.ConfigParser()

write_config.add_section("Order Info")
write_config.set("Order Info",'Action', curr['Action'])
write_config.set("Order Info",'Action Symbol', curr['Action Symbol'])
write_config.set("Order Info",'Ticker', curr['Ticker'])
write_config.set("Order Info",'Strike Price', curr['Strike Price'])
write_config.set("Order Info",'Call Or Put', curr['Call Or Put'])
write_config.set("Order Info",'Expiry Date', curr['Expiry Date'])
write_config.set("Order Info",'Other', ' '.join(curr['Other']))
write_config.set("Order Info",'Limit Price', curr['Limit Price'])



order_path = './orders/'
cfgfile = open(join(order_path, "test_{}.ini".format(todays_date)),'w')
write_config.write(cfgfile)
cfgfile.close()






