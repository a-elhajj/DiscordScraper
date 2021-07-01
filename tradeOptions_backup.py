#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 19:23:22 2021

@author: alexanderel-hajj
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
#from threading import Timer
import threading
#import threading
import time

"""
Parameters
Note: Could be collected from discord.py, sent to .ini file
.ini file can be imported here and used instead of below list
"""
Ticker = 'AAPL'
SecurityType = 'OPT'
ExpiryDate = '20210716'
StrikePrice = 140
CallOrPut = 'C'
Currency = 'USD'
#PrimaryExch = 'NASDAQ'
Action = 'BUY'
Quantity = 1
OrderType = 'LMT'
ValidTime = 'DAY'
AllOrNone = True
LimitPrice = 0.70
AuxPrice = 0
Transmit = True

class IBapi(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self, self)
        
    def error(self, reqId , errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)
        
    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
    
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)
    
    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
    
    def contractDetails(self, reqId: int, contractDetails):
        """
        The first function is contractDetails: a function of the EWrapper. 
        When we request contract details, it will get returned here.
        
        We will store whatever is returned here in a dictionary file.
        The request id, or reqId, that we use to make the request,
        will be used as the key value for the dictionary.
        """
        self.contract_details[reqId] = contractDetails
        
    # Use the reqContractDetails functions of the API. 
    # It will return a contract with the ConID already filled in.
    def get_contract_details(self, reqId, contract):
        """
        For requesting contract details. 
        To access it, we have to pass through a reqId and 
        the contract that we are requesting details for.
        
        There are a number of things involved in this custom function. 
        1. It makes the request for data;
        2. It creates the variable where the data is stored;
        3. It has some error checking to make sure the data is in fact 
        returned and that there are no problems;
        4. It waits for the data, so other commands are not executed 
        before the data comes in.
        """
        # Create a variable to store our incoming data. Set to None
        # Can check later on if the var has a value to confirm data arrived
        self.contract_details[reqId] = None
        
        # Next, the function will send the request to the API
        self.reqContractDetails(reqId, contract)
        
		#Error checking loop - breaks from loop once contract details are obtained
        # Check to see if our data has arrived. Loop set to run 50 times. 
        # In each iteration, it checks to see if our contract details 
        # have been returned, and if so, the loop is broken.
        for err_check in range(50):
            if not self.contract_details[reqId]:
                time.sleep(0.1)
            else:
                break
		#Raise if error checking loop count maxed out (contract details not obtained)
        # If loop runs a full 50x, meaning it didn’t successfully break out,
        # value of err_check=49. In this case, we raise an exception to alert us that 
        # there is a problem getting the contract details.
        if err_check == 49:
            raise Exception('error getting contract details')
		#Return contract details otherwise
        return self.contract_details[reqId].contract
    
    def start(self,
              Ticker: str, SecurityType: str, ExpiryDate: str, 
              StrikePrice: float, CallOrPut: str, Currency: str,
              Action: str, Quantity: float, OrderType: str, ValidTime: str, 
              AllOrNone: bool, LimitPrice: float, Transmit: bool
              ):
        """
        ######################################################################
        Contract Arguements
        ######################################################################
        Ticker: The underlying's asset symbol. Ex: AAPL (string)
        SecurityType: The security's type: (string)
            STK - stock (or ETF) OPT - option FUT - future IND - index FOP - futures option CASH - forex pair BAG - combo WAR - warrant BOND- bond CMDTY- commodity NEWS- news FUND- mutual fund.
        ExpiryDate: The contract's last trading day or contract month (for Options and Futures). (string)
            Strings with format YYYYMM will be interpreted as the Contract Month 
            YYYYMMDD will be interpreted as Last Trading Day.
        StrikePrice: The option's strike price. (double/float)
        CallOrPut: Either Put or Call (i.e. Options). (string)
            Valid values are P, PUT, C, CALL.
        Currency: The underlying's currency. (string)
        PrimaryExch: The contract's primary exchange. (string)
            For smart routed contracts, used to define contract in case of ambiguity. 
            Should be defined as native exchange of contract.
            CAUSING ISSUES - CURRENTLY REMOVED
        Contract Resources: https://interactivebrokers.github.io/tws-api/classIBApi_1_1Contract.html
        
        ######################################################################
        Order Arguements
        ######################################################################
        Action: BUY, SELL (string)
        Quantity: The number of positions being bought/sold. (double)
        OrderType: The order's type. Ex: Limit Order (LMT), Market Order (MKT)  (string)
        ValidTime: The time in force. (string)
            Day: Valid for the day only.
            GTC - Good until canceled.
            IOC - Immediate or Cancel. Any portion that is not filled as soon as it becomes available in the market is canceled.
            GTD. - Good until Date. It will remain working within the system and in the marketplace until it executes or until the close of the market on the date specified
            OPG - Use OPG to send a market-on-open (MOO) or limit-on-open (LOO) order.
            FOK - If the entire Fill-or-Kill order does not execute as soon as it becomes available, the entire order is canceled.
            DTC - Day until Canceled
        AllOrNone: Indicates whether or not all the order has to be filled on a single execution. (bool)
        LimitPrice: The LIMIT price. Used for limit, stop-limit and relative orders. (double)
            In all other cases specify zero. 
            For relative orders with no limit price, also specify zero.
        AuxPrice: Generic field to contain the stop price for STP LMT orders, trailing amount, etc. (double)
            NOT REALLY NEEDED RIGHT NOW, REMOVED.
        Transmit: Specifies whether the order will be transmitted by TWS. (bool)
            If set to false, the order will be created at TWS but will not be sent.
        Order Resources: https://interactivebrokers.github.io/tws-api/classIBApi_1_1Order.html
        """
        contract = Contract()
        contract.symbol = Ticker   
        contract.secType = SecurityType #OPT
        contract.lastTradeDateOrContractMonth = ExpiryDate #20210716
        contract.strike = StrikePrice #140
        contract.right = CallOrPut # call option #C
        contract.currency = Currency #USD
#        contract.primaryExchange = str(PrimaryExch) #NASDAQ
        contract.exchange = "SMART"
        contract.multiplier = '100'

        #Create order object
        order = Order()
        order.action = Action #BUY
        order.totalQuantity = Quantity # 1
        order.orderType = OrderType #LMT
        order.tif = ValidTime #DAY
        order.allornone = AllOrNone #True
        if order.orderType == 'LMT':
            order.lmtPrice = LimitPrice # verify with options chain first
        order.transmit = Transmit
#        AuxPrice = 0
        
        """
        Verification of limit price here...
        """
        return contract, order
    
    def stop(self):
        self.done = True
        self.disconnect()
        
    def cancel(self):
        self.cancelOrder(self.nextorderId)
        
def main(Ticker: str, SecurityType: str, ExpiryDate: str, StrikePrice: float, 
         CallOrPut: str, Currency: str, 
         Action: str, Quantity: float, OrderType: str, ValidTime: str, 
         AllOrNone: bool, LimitPrice: float, Transmit: bool):
    
    def run_loop():
        	app.run()

    app = IBapi()
    app.connect("127.0.0.1", 7497, 123)

    app.nextorderId = None
    
    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    
    #Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            print('connected')
            break
        else:
            print('waiting for connection')
            time.sleep(1)
            
    contract, order = app.start(
                                Ticker, SecurityType, ExpiryDate, StrikePrice, 
                                CallOrPut, Currency,
                                Action, Quantity, OrderType, ValidTime, AllOrNone, 
                                LimitPrice, Transmit
                                )

    app.placeOrder(app.nextorderId, contract, order)
    app.nextorderId += 1
    
    time.sleep(3)
    app.disconnect()
    

if __name__ == "__main__":
    main(
        Ticker, SecurityType, ExpiryDate, StrikePrice, CallOrPut, Currency, 
        Action, Quantity, OrderType, ValidTime, AllOrNone, 
        LimitPrice, Transmit
        )
    
    
    
    
