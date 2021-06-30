#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 12:58:13 2021

@author: alexanderel-hajj
"""

"""
Application ID: 859477833759719425
Public Key: a41fc154fd3ad7948f456e5a7b99bcada62042b400982723eb6a98872b971d55
Token: ODU5NDc3ODMzNzU5NzE5NDI1.YNtRGw.QLWTlX3GS9OBcvIFYFi7njRJCYo
"""


import discord
import pandas as pd

client = discord.Client()
guild = discord.Guild

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('_'):

        cmd = message.content.split()[0].replace("_","")
        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]





