import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import config

# -------------------------------------------
# Modify the holiday class to
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
    name: str
    date: datetime.datetime

    def __init__(self, name, date):
        if not type(date) is datetime.datetime:
            raise TypeError("Argument date must be a datetime")
        self.name = name
        self.date = date

    def __str__ (self):
        # String output
        # Holiday output when printed.
        format = "%Y-%m-%d"
        return f"{self.name} ({self.date.strftime(format)})"


# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    innerHolidays: list

    def __init__(self):
        self.innerHolidays = []

    def addHoliday(self, holidayObj, printSuccess=True):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        if not type(holidayObj) is Holiday:
            raise TypeError("Argument holidayObj must be a Holiday")
        self.innerHolidays.append(holidayObj)
        if printSuccess:
            format = "%Y-%m-%d"
            print(f"Success\n{holidayObj.name} ({holidayObj.date.strftime(format)}) has been added to the holiday list.\n")

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        for holiday in self.innerHolidays:
            if holiday.name == HolidayName and holiday.date == Date:
                return holiday
        return None

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        for i in range(0, len(self.innerHolidays)):
            if self.innerHolidays[i].name == HolidayName and self.innerHolidays[i].date == Date:
                self.innerHolidays.pop(i)
                print(f"Success:\n{HolidayName} has been removed from the holiday list.\n")
                return

    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        holidays: object

        with open(filelocation, 'r') as f:
            holidays = json.loads(f.read())
        
        format = "%Y-%m-%d"
        for holiday in holidays["holidays"]:
            holidayName = holiday["name"]
            holidayDate = datetime.datetime.strptime(holiday["date"], format)
            self.addHoliday(Holiday(holidayName, holidayDate), False)

    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        holidays = {"holidays": []}
        format = "%Y-%m-%d"
        for holiday in self.innerHolidays:
            holidayObj = {
                "name": holiday.name,
                "date": holiday.date.strftime(format)
            }
            holidays["holidays"].append(holidayObj)
        
        with open(filelocation, 'w') as f:
            f.write(json.dumps(holidays, indent=4))

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/
        # Remember, 2 previous years, current year, and 2 years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.
        currentYear = datetime.datetime.today().year
        years = []
        format = "%b %d %Y"
        for year in range(currentYear - 2, currentYear + 3):
            result = requests.get(f"{config.holidayURL}{year}")
            holidays = BeautifulSoup(result.text, "html.parser")
            rows = holidays.find_all('tr')
            for row in rows:
                try:
                    dateStr = row.th.get_text() + f" {year}"
                    date = datetime.datetime.strptime(dateStr, format)
                    name = row.find_all('td')[1].get_text()
                    if not self.findHoliday(name, date):
                        self.addHoliday(Holiday(name, date), False)
                except:
                    continue

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        holidays = lambda date: \
            date.date.isocalendar()[0] == year and \
            date.date.isocalendar()[1] == week_number
        return list(filter(holidays, self.innerHolidays))

    def displayHolidaysInWeek(self, year, week_number):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week.
        # * Remember to use the holiday __str__ method.
        currentWeekHolidays = self.filter_holidays_by_week(year, week_number)
        print(f"\nThese are the holidays for {year} week #{week_number}:")
        for holiday in currentWeekHolidays:
            print(holiday)
        print()

    def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        raise NotImplementedError()

    def viewCurrentWeek(self, year):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        currentWeekNum = datetime.date.today().isocalendar()[1]
        self.displayHolidaysInWeek(year, currentWeekNum)

def addHoliday(holidays: HolidayList):
    print(
        "Add a Holiday\n" \
        "============="
    )
    format = "%Y-%m-%d"
    name = input("Holiday: ")
    dateStr = input("Date: ")
    while True:
        try:
            date = datetime.datetime.strptime(dateStr, format)
            print()
            holidays.addHoliday(Holiday(name, date))
            break
        except:
            print("Error:\nInvalid date. Please try again.\n")
            dateStr = input(f"Date for {name}: ")

def removeHoliday(holidays: HolidayList):
    print(
        "Remove a Holiday\n" \
        "================"
    )
    format = "%Y-%m-%d"

    name = input("Holiday Name: ")
    while True:
        dateStr = input("Date: ")
        print()
        try:
            date = datetime.datetime.strptime(dateStr, format)
            break
        except:
            print("Error:\nInvalid date. Please try again.\n")
    
    if not holidays.findHoliday(name, date):
        print(f"Error:\n{name} ({dateStr}) not found.\n")
    else:
        holidays.removeHoliday(name, date)

def saveHolidayList(holidays: HolidayList):
    print(
        "Saving Holiday List\n" \
        "===================="
    )
    confirm = input("Are you sure you want to save your changes? [y/n]: ")
    if confirm.lower() == "y":
        holidays.save_to_json(config.jsonFileName)
        print("\nSuccess:\nYour changes have been saved.\n")
        return True
    else:
        print("\nCancelled:\nHoliday list file save cancelled.\n")
        return False

def viewHolidays(holidays: HolidayList):
    print(
        "View Holidays\n" \
        "================="
    )
    year = int(input("Which year?: "))
    week = int(input("Which week? #[1-52, Leave blank for the current week]: ") or 0)
    if not week:
        holidays.viewCurrentWeek(year)
    else:
        holidays.displayHolidaysInWeek(year, week)

def exitManager(holidays: HolidayList, saved: bool):
    print(
        "Exit\n" \
        "====="
    )
    confirm = False
    if saved:
        confirm = input("Are you sure you want to exit? [y/n]: ")
    else:
        confirm = input("Are you sure you want to exit?\nYour changes will be lost.\n[y/n]: ")
    print()
    if confirm:
        print("Goodbye!")
        exit()


def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going.
    print(
        "Holiday Management\n" \
        "===================\n" \
        "Reading and scraping holidays..."
    )

    holidays = HolidayList()
    holidays.read_json(config.jsonFileName)
    holidays.scrapeHolidays()

    print(f"There are {holidays.numHolidays()} holidays stored in the system.")

    option = 0
    saved = False
    while option != 5:
        print(
            "Holiday Menu\n" \
            "================\n" \
            "1. Add a Holiday\n" \
            "2. Remove a Holiday\n" \
            "3. Save Holiday List\n" \
            "4. View Holidays\n" \
            "5. Exit\n"
        )
        option = int(input("Choose an option: "))
        print()
        
        if option == 1:
            addHoliday(holidays)
        elif option == 2:
            removeHoliday(holidays)
        elif option == 3:
            saved = saveHolidayList(holidays)
        elif option == 4:
            viewHolidays(holidays)
        elif option == 5:
            exitManager(holidays, saved)

if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





