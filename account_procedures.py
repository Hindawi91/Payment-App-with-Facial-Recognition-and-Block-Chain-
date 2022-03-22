import pandas as pd
from blockchain import Blockchain
import random

def is_user(user):
    df = pd.read_excel('database.xlsx')  
    customers = list (df.loc[:, 'customer'])
    if user in customers:
        return True
    else:
        return False

def check_balance(user):
    df = pd.read_excel('database.xlsx')  
    customers = list (df.loc[:, 'customer'])
    balances = list (df.loc[:, 'balance'])
    user_idx = customers.index(user)
    balance = balances[user_idx]
    return balance 


def send_money(sender,reciever,amount):
    
    df = pd.read_excel('database.xlsx')  
    customers = list (df.loc[:, 'customer'])
    balances = list (df.loc[:, 'balance'])
    transfer_status = ""
    
    print (df) 
    if sender in customers and reciever in customers:
        
        sender_idx = customers.index(sender)
        reciever_idx = customers.index(reciever)
        
        sender_balance = balances[sender_idx]
        reciever_balance = balances[reciever_idx]
        
        print(f" Sender: {sender}")
        print(f" Balance before transfer: {sender_balance}\n")
              
        print(f" Reciever: {reciever}")
        print(f" Balance before transfer: {reciever_balance}\n")
        
        print (df.iloc[sender_idx][1])
        df.iat[sender_idx,1] = 3000 
        print (df.iloc[sender_idx][1])
        
        if amount > sender_balance:
            transfer_status = "Transfer Error: insufficient funds to complete transfer"
            print (transfer_status)
        else:
            
            blockchain = Blockchain()
            transaction = blockchain.new_transaction(sender, reciever, amount)
            proof_no = random.randint(0,999999999999999)
            blockchain.new_block(proof_no)
    
            
            
            new_sender_balance = sender_balance - amount
            new_reciever_balance = reciever_balance + amount
            
            df.iat[sender_idx,1] = new_sender_balance
            df.iat[reciever_idx,1] = new_reciever_balance
            
            transfer_status = "Transfer Successful"
            
            df.to_excel("database.xlsx",sheet_name='Sheet_name_1',index=False)
            print (transfer_status)
           
            print(df)
    return transfer_status


if __name__ == "__main__":
    sender = "Firas Al-Hindawi"
    reciever = "Khabib"
    send_money(sender,reciever,300)