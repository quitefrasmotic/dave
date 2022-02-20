import math
import datetime

def calculate_price():
        input_prices = [2638/100, 28.77, 17.63] # cocoa, milk, sugar
        weights = [0.4, 0.4, 0.2]
        input_adjusted = []
        if sum(weights) == 1.0:
            for i in range(len(input_prices)):
                weight_adjusted_value = input_prices[i] * weights[i]
                input_adjusted.append(weight_adjusted_value)
            print("weight-adjusted input prices: " + str(input_adjusted))
        
        input_market_caps = [i * 1000000 for i in input_adjusted]
        input_caps_product = sum(input_market_caps)
        outstanding_shares = 1000000
        share_price = input_caps_product / outstanding_shares

        print("market cap: $"+str(int(input_caps_product))) # 67.780.000
        print("outstanding shares: "+str(outstanding_shares))
        print(f"share price: ${str(share_price)[:5]}") # 25

        your_holdings = 0
        your_balance = 1000000
        print("your holdings: "+str(your_holdings))
        print("your balance: $"+str(your_balance))
        decision = input(f"\nbuy or sell #? (buy #/sell #) ")

        past_trades = []
        while True:
            if "buy" in decision:
                args = decision.split(" ") # make sure share amount is an integer
                your_balance -= float(args[1]) * share_price
                recent_trades = 0
                for i in range(len(past_trades)): # trade price is influenced primarily by volume (demand)
                    if past_trades[i][0] > (datetime.datetime.utcnow() - datetime.timedelta(minutes=1)):
                        print(f"trade {i} in last 10 mins")
                        recent_trades += 1
                share_price += (0.01 * recent_trades)
                your_holdings += float(args[1])
            elif "sell" in decision:
                args = decision.split(" ")
                your_balance += float(args[1]) * share_price
                share_price -= float(args[1]) * 0.0001
                your_holdings -= float(args[1])
            
            past_trades.append([datetime.datetime.utcnow(),share_price])
            print(f"share price: ${str(share_price)[:5]}")
            print("your holdings: "+str(int(your_holdings)))
            print("your balance: $"+str(your_balance))
            decision = input(f"\nbuy or sell #? (buy #/sell #) ")

calculate_price()
