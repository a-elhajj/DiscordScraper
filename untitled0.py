#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 12:58:13 2021

@author: alexanderel-hajj
"""

"""
Application ID: HERE
Public Key: HERE
Token: HERE
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





