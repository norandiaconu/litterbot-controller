#!/usr/bin/env python3
import asyncio
from pylitterbot import Account
from datetime import date

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
  print("Logging in...")
  dateStr = str(date.today())
  account = Account()
  try:
    await account.connect(username=username, password=password, load_robots=True)
    for robot in account.robots:
      print("Robot:", robot.name, "("+robot.model+")")
      print("Current status:", robot.status)
      history = await robot.get_activity_history()
      eventsToday = 0
      for event in history:
        eventStr = str(event)
        if eventStr.startswith(dateStr):
          eventsToday += 1
      print("Events today:", eventsToday)
      next = input("""
      Enter one of the following numbers to continue or anything else to disconnect:
      1) Cycle litterbot
      2) View history
      3) View insight
      """)
      if next == "1":
        await robot.start_cleaning()
        print("Started cycle...")
      elif next == "2":
        for event in history:
          print(event)
      elif next == "3":
        insight = await robot.get_insight()
        print(insight)
  finally:
    print("Disconnecting...")
    await account.disconnect()

if __name__ == "__main__":
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  main()
