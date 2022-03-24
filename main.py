import PySimpleGUI as sg
from face_rec import get_facename
from account_procedures import check_balance, send_money, is_user

sg.theme('TanBlue')

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
        [sg.Text("Enter payment amount in Crypto Currency", key="new")],
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
        [sg.Text(f"Balance: {user_balance} Crypto Currency", key="balance")],
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
            window['balance'].Update(f"Balance: {user_balance} Crypto Currency")
            
            
    window.close()
    
  
main_layout = [
    [sg.Image(filename=r'output-onlinepngtools.png',background_color='white')],
    [sg.Button(button_text="Login using face ID",size=(20,2))],
    [sg.Button(button_text="Exit",size=(20,2))]
    ]   

  
def main():
    window = sg.Window("Main Window", layout = main_layout,background_color= 'white',element_justification='c')
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