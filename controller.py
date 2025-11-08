#!/usr/bin/env python3
import asyncio
import time
from pylitterbot import Account
from datetime import date
from yaspin import yaspin

robot = None
history = None
spinner = yaspin()

def main():
    try:
        import config
        username = config.username
        password = config.password
        asyncio.run(login(username, password))
    except ModuleNotFoundError:
        print("No config found, please enter the following")
        f = open("config.py", "w")
        username = input("Username:")
        f.write("username = '" + username + "'\n")
        password = input("Password:")
        f.write("password = '" + password + "'")
        f.close()
        main()

async def login(username, password):
    spinner.text = "Logging in..."
    spinner.start()
    dateStr = str(date.today())
    account = Account()
    try:
        await account.connect(username=username, password=password, load_robots=True)
        loadedOnce = 'False'
        for eachRobot in account.robots:
            global robot
            robot = eachRobot
            spinner.stop()
            print("Robot:", robot.name, "("+robot.model+")")
            print("Current status:", robot.status)
            spinner.text = "Getting activity history..."
            spinner.start()
            try:
                global history
                if loadedOnce == 'True':
                    time.sleep(2)
                history = await robot.get_activity_history()
                loadedOnce = 'True'
            except:
                print("ERROR")
            eventsToday = 0
            for event in history:
                eventStr = str(event)
                if eventStr.startswith(dateStr):
                    eventsToday += 1
            spinner.stop()
            print("Events today:", eventsToday)
            await controls()
    finally:
        spinner.text = "Disconnecting..."
        await account.disconnect()
        spinner.stop()

async def controls():
    next = input("""
        Enter one of the following numbers to continue or anything else to disconnect:
        1) Cycle litterbot
        2) Reset status
        3) View history
        4) View cat weights
        -> """)
    if next == "1":
        spinner.text = "Starting cycle..."
        spinner.start()
        await robot.start_cleaning()
        spinner.stop()
        print("Started cycle")
        await controls()
    elif next == "2":
        spinner.text = "Status resetting..."
        spinner.start()
        await robot.reset()
        spinner.stop()
        print("Status reset")
        await controls()
    elif next == "3":
        for event in history:
            print(str(event.timestamp.replace(tzinfo=None)) + " - " + str(event.action))
        await controls()
    elif next == "4":
        cat1Weights = []
        cat1Times = []
        cat2Weights = []
        cat2Times = []
        for event in history:
            if "Pet Weight Recorded: " in str(event.action):
                weight = float(event.action[21:26])
                if weight >= 15.0:
                    cat2Weights.append(weight)
                    cat2Times.append(event.timestamp)
                elif weight >= 10.0:
                    cat1Weights.append(weight)
                    cat1Times.append(event.timestamp)
        print("Cat 1 weights (lbs):")
        i = 0
        for cat1 in cat1Weights:
            print(str(cat1Times[i].replace(tzinfo=None)) + " - " + str(cat1))
            i += 1
        print ("Cat 2 weights (lbs):")
        i = 0
        for cat2 in cat2Weights:
            print(str(cat2Times[i].replace(tzinfo=None)) + " - " + str(cat2))
            i += 1
        await controls()

if __name__ == "__main__":
    main()
