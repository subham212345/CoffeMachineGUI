from tkinter import *
from datetime import date, datetime

today = date.today()
now = datetime.now()
window = Tk()
window.title("Coffee Machine")
window.config(height=600, width=400, padx=25, pady=25)

date_today = today.strftime("%b-%d-%Y")
date_time = now.strftime("%H:%M:%S")
# Creating the menu
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

profit = 0
resources = {
    "water": 3000,
    "milk": 2000,
    "coffee": 1000,
}


# To refill the resources
def reset_resources():
    global resources
    resources = {
        "water": 3000,
        "milk": 2000,
        "coffee": 1000,
    }
    message_result.config(text="The resources have been reset. \n"
                               "Please select your order")


# To check if sufficient resources are left
def check_resources(menu_name):
    if menu_name == "latte" or menu_name == "cappuccino":
        if MENU[menu_name]["ingredients"]["milk"] > resources["milk"]:
            message_result.config(text="Insufficient milk")

    if MENU[menu_name]["ingredients"]["water"] > resources["water"]:
        message_result.config(text="Insufficient water")

    elif MENU[menu_name]["ingredients"]["coffee"] > resources["coffee"]:
        message_result.config(text="Insufficient coffee")
        return False
    else:
        message_result.config(text="Your order is being prepared")
        drink = MENU[menu_name]
        print(type(drink))
        update_resources(menu_name, drink["ingredients"])


def update_resources(drink_name, order_ingredient):
    for item in order_ingredient:
        resources[item] -= order_ingredient[item]
    message_result.config(text=f"Here is your {drink_name} ☕️. Enjoy!")



def off():
    message_result.config(text="The machine has turned off!! \n"
                               "Turn it on from the options tab at top left of the window")
    lines = str(date_today) + " : " + str(date_time) + "---" + str(profit)
    with open('collection_logs.txt', 'a') as f:
        f.writelines(lines)
        f.write('\n')
    latte_button.config(state=DISABLED)
    espresso_button.config(state=DISABLED)
    cappuccino_button.config(state=DISABLED)
    report_button.config(state=DISABLED)
    refill_button.config(state=DISABLED)
    off_button.config(state=DISABLED)


def menu_choice(a):
    global profit

    menu_name = ""
    if a == "latte":
        menu_name = "latte"
        profit += 2.5
    elif a == "espresso":
        menu_name = "espresso"
        profit += 1.5
    elif a == "cappuccino":
        menu_name = "cappuccino"
        profit += 3.0
    check_resources(menu_name)


def report():
    message_result.config(text="Here is the remaining resources \n"
                               f"There is {resources['water']} ml water left. \n"
                               f"There is {resources['milk']} ml milk left. \n"
                               f"There is {resources['coffee']} gram coffee left. \n"
                               f"Money: ${profit}")


# Canvas for image
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="coffee.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=1)


def turn_on():
    # Button for coffee menu
    global latte_button,  espresso_button, cappuccino_button,  off_button, refill_button, report_button, message_result
    latte_button = Button(text="Latte($2.5)", command=lambda: menu_choice("latte"), width=15)
    latte_button.grid(column=0, row=2)

    espresso_button = Button(text="Espresso($1.5)", command=lambda: menu_choice("espresso"), width=15)
    espresso_button.grid(column=1, row=2)

    cappuccino_button = Button(text="Cappuccino($3.0)", command=lambda: menu_choice("cappuccino"), width=15)
    cappuccino_button.grid(column=2, row=2)

    # Buttons to turn it off and refill resources and generate report
    off_button = Button(text="Turn Off", command=lambda : off(), width=15)
    off_button.grid(column=0, row=0)

    refill_button = Button(text="Refill Resource", command=lambda: reset_resources(), width=15)
    refill_button.grid(column=1, row=0)

    report_button = Button(text="Report", command=lambda: report(), width=15)
    report_button.grid(column=2, row=0)

    # Display message
    message_result = Label(window, text="Choose one of the menu", font=("arial", 20, "bold"), fg="black", height=8, width=50)
    message_result.grid(row=4, column=1)


menu = Menu(window)
window.config(menu=menu)

# Create options for menu
options = Menu(menu, tearoff=False)
menu.add_cascade(label="Options", menu=options)
options.add_command(label="Turn the machine ON", command=turn_on)

turn_on()

window.mainloop()
