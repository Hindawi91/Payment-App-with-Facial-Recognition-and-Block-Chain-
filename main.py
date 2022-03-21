import PySimpleGUI as sg
from face_rec import get_facename
from account_procedures import check_balance, send_money, is_user

def msg_box(msg):
    layout = [
        [sg.Text(msg, key="new")],
        [sg.Button("close")]
        ]
    
    window = sg.Window("Message Box", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "close" or event == sg.WIN_CLOSED:
            break
            
    window.close()

def payment_window(user_name):
    layout = [
        [sg.Text("Enter receiver name:", key="new")],
        [sg.InputText()],
        [sg.Text("Enter payment amount in Dollars $", key="new")],
        [sg.InputText()],
        [sg.Button("Send Money"),sg.Button("Exit")],
        ]
    
    window = sg.Window("Payment Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            
            break
        
        if event == "Send Money":
            reciever = values[0]
            
            try:
                amount = float(values[1])
            except ValueError:
                msg_box('Please enter a valid numerical amount')
            
            if is_user(reciever) == True and isinstance(amount, (int, float)) == True:
                Payment_status = send_money(user_name,reciever,amount)
                msg_box(Payment_status)
                
            elif is_user(reciever) == False:
                msg_box(f'{reciever} is not a registered user')
                
            elif isinstance(amount, (int, float)) == False:
                msg_box('Please enter a valid numerical amount')
                
    window.close()


def balance_window(user_name,user_balance):
    layout = [
        [sg.Text(f"Customer Name: {user_name}", key="customer")],
        [sg.Text(f"Balance: ${user_balance}", key="balance")],
        [sg.Button("Make Payment"),sg.Button("Refresh"),sg.Button("Exit")]
        ]
    
    window = sg.Window("Balance Window", layout, modal=True)
    choice = None
    
    while True:
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        if event == "Make Payment":
            payment_window(user_name)
            
        if event == "Refresh":
            
            user_balance = check_balance(user_name)
            window['balance'].Update(f"Balance: ${user_balance}")
            
            
    window.close()
    
  
main_layout = [
    [sg.Text("hello from PySimpleGUI")],
    [sg.Button("Login using face ID")],
    [sg.Button("Exit")]
    ]   
  
  
def main():
    window = sg.Window("Main Window", layout = main_layout, size = (500,500))
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
            
        if event == "Login using face ID":
            user_name = get_facename()
            user_balance = check_balance(user_name)
            
        
            print(f"user_name: {user_name}")
            print(f"user_balance = {user_balance}")
            
            balance_window(user_name,user_balance)
            
    window.close()
    
    
if __name__ == "__main__":
    main()