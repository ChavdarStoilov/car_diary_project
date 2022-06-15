import PySimpleGUI as sg
import os
from datetime import date

today = date.today()
the_date = today.strftime("%d.%m.%Y")
users_path = os.getcwd() + '\\users_files\\'


# Function for checking users
def check_user(the_values):
    try:
        with open("users/username.txt", "r") as users:
            with open("users/passwords.txt", "r") as passwords:
                range_of_users = users.readlines()
                range_of_password = passwords.readlines()
                if f"{the_values[0]}\n" in range_of_users:
                    for index in range(len(range_of_users)):
                        if f"{the_values[0]}\n" == range_of_users[index] and range_of_password[index] == f"{the_values[1]}\n":
                            login_page(the_values)
                            break
                    else:
                        not_found_user = window['message2'].update("Wrong User or Password")
                        return not_found_user
                else:
                    not_found_user = window['message2'].update("Wrong User or Password")
                    return not_found_user
    except:
        not_found_user = window['message2'].update("Wrong User or Password")
        return not_found_user


# Function for registration
def registration(the_value):
    with open("users/username.txt", "r") as users:
        if the_value[2] == "" or the_value[3] == "":
            text = window['message']
            not_successful = text.update('Please add correct user and password')
            return not_successful
        elif the_value[2] in users.read():
            return window['message'].update("Тhe user already exists")
        else:
            with open("users/username.txt", "a+") as user:
                user.write(f"{the_value[2]}\n")
                user.close()
            with open("users/passwords.txt", "a+") as passwd:
                passwd.write(f"{the_value[3]}\n")
                passwd.close()

                text = window['message']
                successful = text.update('Registration successful')
                window["Register me"].update(visible=False)

                user_folder = users_path + the_value[2]
                os.mkdir(user_folder)
                folder_fuel = users_path + the_value[2] + '\\fuel_files'
                os.mkdir(folder_fuel)
                folder_service = users_path + the_value[2] + '\\service_files'
                os.mkdir(folder_service)

                return successful





# Function for user log page
def login_page(user):
    window['-COL2-'].update(visible=False)
    window['-COL4-'].update(visible=True)
    return window['welcome'].update(f"Hello {user[0]}")


# Function for adding service data
def the_service_diary_adding(the_values):
    user = window['welcome'].get()
    the_user = user[6:]
    folder_service = users_path + the_user + '\\service_files\\'

    if f"{the_values[4]}.txt" in folder_service:
        return window['add_message2'].update('\t\tAlready have records on this date')

    else:
        try:
            if the_values[8] == "" or the_values[9] == "" or the_values[10] == "" or \
                    the_values[11] == "" or the_values[12] == "":
                return window['add_message2'].update('\t\tPlease write correct data in the fields')
            else:
                with open(f"{folder_service}\\{the_values[8]}.txt", "a+") as service:
                    service.write(
                        f"Date: {the_values[8]}:\n\nType service: {the_values[9]}\nService station: {the_values[10]}\n"
                        f"Kilometers traveled: {int(the_values[11])}\nAmount: {int(the_values[12])} lv.\n\n")
                    service.close()

                return window['add_message2'].update('\t\t\tAdded Successful.')
        except:
            return window['add_message2'].update('\t\tPlease write correct data in the fields')


# Function for showing service data
def the_service_diary_showing(file):
    user = window['welcome'].get()
    the_user = user[6:]

    folder_service = users_path + the_user + '\\service_files\\'

    try:
        with open(f"{folder_service}{file}.txt") as service:
            window['service'].update(visible=False)
            window['service_info'].update(f"{service.read()}")

    except:
        window['service'].update(visible=False)
        return window['service_info'].update("Do not have added files")


# Function for adding new fuel data
def the_fuel_dairy_adding(the_values):
    user = window['welcome'].get()
    the_user = user[6:]
    folder_fuel = users_path + the_user + '\\fuel_files\\'

    if f"{the_values[4]}.txt" in folder_fuel:
        return window['add_message'].update('\t\tAlready have records on this date')

    else:
        try:
            if the_values[4] == "" or the_values[5] == "" or the_values[6] == "":
                return window['add_message'].update('\t\tPlease write correct data in the fields')
            else:
                average_consumption = (int(the_values[5]) / 10) / (int(the_values[6]) / 10)
                with open(f"{folder_fuel}\\{the_values[4]}.txt", "a+") as fuel:
                    fuel.write(f"Date: {the_values[4]}:\n\nDistance: {the_values[5]}\nLiters: {the_values[6]}\n"
                               f"Gas Station: {the_values[7]}\nAverage consumption: {average_consumption:.2f}\n\n")
                    fuel.close()

                return window['add_message'].update('\t\t\tAdded Successful.')
        except:
            return window['add_message'].update('\t\tPlease write correct data in the fields')


# Function for showing fuel data
def the_fuel_dairy_showing(file):
    user = window['welcome'].get()
    the_user = user[6:]

    folder_fuel = users_path + the_user + '\\fuel_files\\'
    try:
        with open(f"{folder_fuel}{file}.txt") as fuel:
            window['fuel'].update(visible=False)
            window['fuel_info'].update(f"{fuel.read()}")
    except:
        window['fuel'].update(visible=False)
        return window['fuel_info'].update("Do not have added files")

# Function to get all files for Fuel
def get_files_fuel():
    try:
        user = window['welcome'].get()
        folder_fuel = users_path + user[6] + '\\fuel_files\\'
        the_fuel_folder = os.listdir(folder_fuel)
        window['fuel'].update(values=[i[:-4:] for i in the_fuel_folder])
    except:
        window['service'].update(values="")


# Function to get all files for service
def get_files_service():
    try:
        user = window['welcome'].get()
        folder_service = users_path + user[6] + '\\service_files\\'
        the_service_folder = os.listdir(folder_service)
        window['service'].update(values=[i[:-4:] for i in the_service_folder])
    except:
        window['service'].update(values="")


theme = "DarkGrey6"
sg.theme(theme)  # Add a touch of color

# All the stuff inside your window.

# Main layout
main_layout = [
    [sg.Text('\t         '), sg.Text("Welcome to Car Dairy", font="Arial, 15", justification='center')],
    [sg.Text('\n\n\n\n\n\n\n')],
    [sg.Button('Login ', size=(50, 1))],
    [sg.Button('Registration', size=(50, 1))],
    [sg.Text('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')],
    [sg.Text('\t\t  '), sg.Button('Close', size=(15, 1))]
]

# Login layout
login_layout = [
    [sg.Text('\t\t\t'), sg.Text("Login", font="Arial, 25")],
    [sg.Text('\n\n\n\n\n')],
    [sg.Text('\t'), sg.Text('', key="message2", font="Arial, 15")],
    [sg.Text('\n')],
    [sg.Text('Username', size=(10, 1)), sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('Password', size=(10, 1)),
     sg.InputText('', password_char='*', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('\n\n')],
    [sg.Button('Enter', size=(55, 1), )],
    [sg.Text('\n\n\n\n\n\n')],
    [sg.Text('\t  '), sg.Button('Back', size=(35, 1))]
]

# Registration layout
registration_layout = [
    [sg.Text('\t\t'), sg.Text("Registration", font="Arial, 25")],
    [sg.Text('\n\n\n\n\n')],
    [sg.Text('\t'), sg.Text('', key='message', font="Arial, 15")],
    [sg.Text('\n')],
    [sg.Text('Username', size=(10, 1)), sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('Password', size=(10, 1)),
     sg.InputText('', password_char='*', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('\n\n')],
    [sg.Button('Register me', size=(55, 1), )],
    [sg.Text('\n\n\n\n\n\n')],
    [sg.Text('\t  '), sg.Button('Back', size=(35, 1))]
]

# After login layout
login_page_layout = [
    [sg.Text("\t"), sg.Text('', key='welcome', font="Arial, 15")],
    [sg.Text('\n\n\n')],
    [sg.Button('Service Dairy', size=(25, 1))],
    [sg.Text('\n')],
    [sg.Button('Fuel Dairy', size=(25, 1))],
    [sg.Text('\n\n\n\n\n\n\n\n\n\n\n')],
    [sg.Button('LogOut', size=(25, 1))]

]

# The service daily layout
service_diary_layout = [
    [sg.Text('\t'), sg.Text('Service diary', font="Arial, 15")],
    [sg.Text('\n\n\n')],
    [sg.Button("Adding new service activity", size=(25, 1))],
    [sg.Text('\n')],
    [sg.Button("Show service activity", size=(25, 1))],
    [sg.Text('\n\n\n\n\n\n\n\n\n\n\n')],
    [sg.Button('Back', size=(25, 1))]

]

# The Fuel dairy layout
fuel_dairy_layout = [
    [sg.Text('\t'), sg.Text('Fuel diary', font="Arial, 15")],
    [sg.Text('\n\n\n')],
    [sg.Button("Adding new fuel charging", size=(25, 1))],
    [sg.Text('\n')],
    [sg.Button("Show fuel charging", size=(25, 1))],
    [sg.Text('\n\n\n\n\n\n\n\n\n\n\n')],
    [sg.Button('Back', size=(25, 1))]
]

#  The Fuel showing layout
fuel_dairy_showing_layout = [
    [sg.Text('\t\t'), sg.Text('Fuel charging show', font="Arial, 15")],
    [sg.Text('\n\n\n')],
    [sg.Text('\t\t'), sg.Listbox(values='', select_mode='extended', key='fuel', size=(30, 6), visible=True)],
    [sg.Text('\n\n\n\t'), sg.Text("", key="fuel_info", font="Arial, 17")],
    [sg.Text('\n\n\n\n\n\n')],
    [sg.Button("Show", size=(25, 1)), sg.Button('Back', size=(25, 1))]
]

# The Service showing layout
service_showing_layout = [
    [sg.Text('\t\t'), sg.Text('Show service activity', font="Arial, 15")],
    [sg.Text('\n\n\n')],
    [sg.Text('\t\t'), sg.Listbox(values='', select_mode='extended', key='service', size=(30, 6), visible=True)],
    [sg.Text('\n\n\n\t'), sg.Text("", key="service_info", font="Arial, 17")],
    [sg.Text('\n\n\n\n\n\n')],
    [sg.Button("Show", size=(25, 1)), sg.Button('Back', size=(25, 1))]
]

# The Service adding layout
service_adding_layout = [
    [sg.Text('\t'), sg.Text('Add new service activity', font="Arial, 15")],
    [sg.Text('\n\n\n\n\n')],
    [sg.Text('', key='add_message2')],
    [sg.Text('\n\n')],
    [sg.CalendarButton('Today', format="%d.%m.%Y", size=(9, 1)),
     sg.Input(size=(50, 1), do_not_clear=False, justification='center')],
    [sg.Text('Type service', size=(10, 1)), sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('Service station', size=(10, 1)),
     sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('Kilometers traveled', size=(10, 1)),
     sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('Amount', size=(10, 1)), sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('\n\n\n')],
    [sg.Button("Save", size=(25, 1)), sg.Button('Back', size=(25, 1))]
]

# The Fuel adding layout
fuel_adding_layout = [
    [sg.Text('\t'), sg.Text('Add new fuel charging', font="Arial, 15")],
    [sg.Text('\n\n\n\n\n')],
    [sg.Text('', key='add_message')],
    [sg.Text('\n\n')],
    [sg.CalendarButton('Today', format="%d.%m.%Y", size=(9, 1)),
     sg.Input(size=(50, 1), do_not_clear=False, justification='center')],
    [sg.Text('Distance', size=(10, 1)), sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('Liters', size=(10, 1)), sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('Gas station', size=(10, 1)), sg.InputText('', size=(50, 1), justification='center', do_not_clear=False)],
    [sg.Text('\n\n\n')],
    [sg.Button("Save", size=(25, 1)), sg.Button('Back', size=(25, 1))]
]

# layout configure
the_layout = [
    [sg.Column(main_layout, key='-COL1-'),
     sg.Column(login_layout, visible=False, key='-COL2-'),
     sg.Column(registration_layout, visible=False, key='-COL3-'),
     sg.Column(login_page_layout, visible=False, key='-COL4-'),
     sg.Column(service_diary_layout, visible=False, key='-COL5-'),
     sg.Column(fuel_dairy_layout, visible=False, key='-COL6-'),
     sg.Column(service_showing_layout, visible=False, key='-COL7-'),
     sg.Column(fuel_dairy_showing_layout, visible=False, key='-COL8-'),
     sg.Column(fuel_adding_layout, visible=False, key='-COL9-'),
     sg.Column(service_adding_layout, visible=False, key='-COL10-')]
]

# Create the Window
window = sg.Window('Your car diary', the_layout, size=(550, 550), element_justification='center')
# Event Loop to process "events" and get the "layout" of the inputs


while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Close':
        break
    elif event == 'Login ':
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=True)
    elif event == 'Registration':
        window['-COL1-'].update(visible=False)
        window['-COL3-'].update(visible=True)

    if event == "Enter":
        check_user(values)

    elif event == "Register me":
        registration(values)

    elif event == "Service Dairy":
        window['-COL4-'].update(visible=False)
        window['-COL5-'].update(visible=True)

    elif event == "Fuel Dairy":
        window['-COL4-'].update(visible=False)
        window['-COL6-'].update(visible=True)

    if event == "Show service activity":
        window['-COL5-'].update(visible=False)
        window['-COL7-'].update(visible=True)
        get_files_service()

    if event == "Show fuel charging":
        window['-COL6-'].update(visible=False)
        window['-COL8-'].update(visible=True)
        get_files_fuel()

    if event == "Adding new service activity":
        window['-COL5-'].update(visible=False)
        window['-COL10-'].update(visible=True)
    elif event == "Adding new fuel charging":
        window['-COL6-'].update(visible=False)
        window['-COL9-'].update(visible=True)

    if event == "LogOut":
        window['-COL4-'].update(visible=False)
        window['-COL2-'].update(visible=True)

    # Checking for Back buttons
    if event == "Back":
        window['-COL2-'].update(visible=False)
        window['-COL1-'].update(visible=True)
        window['message2'].update("")
    elif event == "Back0":
        window['-COL3-'].update(visible=False)
        window['-COL1-'].update(visible=True)
        window["Register me"].update(visible=True)
        window['message'].update("")
    elif event == "Back1":
        window['-COL5-'].update(visible=False)
        window['-COL4-'].update(visible=True)
    elif event == "Back2":
        window['-COL6-'].update(visible=False)
        window['-COL4-'].update(visible=True)
    elif event == "Back3":
        window['-COL7-'].update(visible=False)
        window['-COL5-'].update(visible=True)
        window['service'].update(visible=True)
        window['service_info'].update("")
    elif event == "Back5":
        window['-COL8-'].update(visible=False)
        window['-COL6-'].update(visible=True)
        window['fuel'].update(visible=True)
        window['fuel_info'].update("")
    elif event == "Back6":
        window['-COL9-'].update(visible=False)
        window['-COL6-'].update(visible=True)
        window['add_message'].update("")
    elif event == "Back9":
        window['-COL10-'].update(visible=False)
        window['-COL5-'].update(visible=True)
        window['add_message2'].update("")

    if event == "Save":
        the_fuel_dairy_adding(values)
    elif event == "Save8":
        the_service_diary_adding(values)

    if event == "Show":
        the_file = ""
        for val in values['service']:
            the_file = the_file + val

        the_service_diary_showing(the_file)

    elif event == "Show4":
        the_file = ""
        for val in values['fuel']:
            the_file = the_file + val

        the_fuel_dairy_showing(the_file)

window.close()
