import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from string import capwords



### Importing provided holiday list

fn = 'holidays.json'
with open(fn, 'r') as f:
    holi_tmp = json.load(f)

holidays_Provided = holi_tmp['holidays']
for holiday in holidays_Provided:
    holiday['year'] = int(holiday['date'][0:4])
    holiday['month'] = int(holiday['date'][6:7])
    holiday['day'] = int(holiday['date'][8:10])
    del holiday['date']



### Scraping Holidays and adding to holidays_Final list. 

def month_Str2Int(monthStr):
    if monthStr == "Jan":
        return 1
    elif monthStr == "Feb":
        return 2
    elif monthStr == "Mar":
        return 3
    elif monthStr == "Apr":
        return 4
    elif monthStr == "May":
        return 5
    elif monthStr == "Jun":
        return 6
    elif monthStr == "Jul":
        return 7
    elif monthStr == "Aug":
        return 8
    elif monthStr == "Sep":
        return 9
    elif monthStr == "Oct":
        return 10
    elif monthStr == "Nov":
        return 11
    elif monthStr == "Dec":
        return 12

def getHTML(url):
    response = requests.get(url)
    return response.text

datehtml_2020 = getHTML('https://www.timeanddate.com/holidays/us/2020')
datehtml_2021 = getHTML('https://www.timeanddate.com/holidays/us/2021')
datehtml_2022 = getHTML('https://www.timeanddate.com/holidays/us/2022')
datehtml_2023 = getHTML('https://www.timeanddate.com/holidays/us/2023')
datehtml_2024 = getHTML('https://www.timeanddate.com/holidays/us/2024')

holiday_years = {'2020': datehtml_2020,
                 '2021': datehtml_2021,
                 '2022': datehtml_2022,
                 '2023': datehtml_2023,
                 '2024': datehtml_2024
                }

holidays_Final = []
                 
for k,v in holiday_years.items():
    datesoup = BeautifulSoup(v, 'html.parser')
    
    holi_table = datesoup.find('section', attrs = {'class':'table-data__table'})
    holi_body = holi_table.find('tbody')
    
    holidaysRaw = []
    for row in holi_body.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 0:
            holiday = {}
            holiday['name'] = cells[1].string
            holiday['type'] = cells[2].string
            holidaysRaw.append(holiday)
        
    holiday_dates = []
    for row in holi_body.find_all('tr'):
        cells = row.find_all('th')
        if len(cells) > 0:
            holiday_dates.append(cells[0].string)

    for i in range (len(holidaysRaw)):
        holidaysRaw[i]['year'] = int(k)
        holidaysRaw[i]['month'] = month_Str2Int(holiday_dates[i][0:3])
        holidaysRaw[i]['day'] = int(holiday_dates[i][4:6])
        
    holiday_noRepeats = []
    for i in range(len(holidaysRaw)):
        if holidaysRaw[i]["name"] not in holiday_noRepeats:
            holidays_Final.append(holidaysRaw[i])
            holiday_noRepeats.append(holidaysRaw[i]["name"])

holidays_Final.extend(holidays_Provided)

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self, name, year, month, day): 
        self.name = name
        self.date = datetime.date(year, month, day)
        self.year = year
    
    def __str__ (self):
        return f'{self.name} on {self.date}'
    
    

# Adding holidays_Final in as Holiday objects

def add_holidays():
    global holidays_Final
    global holiday_list

    holiday_list = [Holiday(holidays_Final[i]["name"], int(holidays_Final[i]["year"]), int(holidays_Final[i]["month"]), int(holidays_Final[i]["day"])) for i in range(len(holidays_Final))]


add_holidays()


# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:
    def __init__(self):
        self.innerHolidays = []
    
    def addHoliday(self, holidayObj): 
        if isinstance(holidayObj, Holiday) == True:
            self.innerHolidays.append(holidayObj)
            print(f"{str(holidayObj.name)} on {str(holidayObj.date)} was successfully added. \n")
        else:
            print("Error")
        
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
 
    def findHoliday(self, HolidayName): 
        tmp_list = []
        for i in range(len(self.innerHolidays)):
            if self.innerHolidays[i].name == HolidayName:
                tmp_list.append(self.innerHolidays[i])
        
        return tmp_list
                
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, HolidayName, Year):
        any_deleted = False
        for i in range(len(self.innerHolidays)):
            if str(self.innerHolidays[i].name) == HolidayName and int(self.innerHolidays[i].year) == Year:
                any_deleted = True
                del self.innerHolidays[i]
                print(f"{HolidayName} for the year {Year} successfully removed.")
                break
            
        if any_deleted == False:
            print(f"Error: Holiday not removed because {HolidayName} for the year {Year} not found.")
            
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        
        
#     def read_json(filelocation):
#         # Read in things from json file location
#         # Use addHoliday function to add holidays to inner list.
#         pass

    def save_to_json(fileName):
        # Write out json file to selected file.
        
        toExport={"Holidays":[]}

        for i in range(len(h1.innerHolidays)):
            holiday = {}
            holiName = h1.innerHolidays[i].name
            holiDate = str(h1.innerHolidays[i].date)
            holiday["name"] = holiName
            holiday["date"] = holiDate
            toExport["Holidays"].append(holiday)
    
        
        fn = str(fileName)
        with open(fn, 'w') as f:
            json.dump(toExport, f, indent = 4)
        
        print(f"File successfully saved as {fn}.")
        
         
#     def scrapeHolidays():
#         # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
#         # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
#         # Check to see if name and date of holiday is in innerHolidays array
#         # Add non-duplicates to innerHolidays
#         # Handle any exceptions.     
#         pass

    def numHolidays(self):
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(year, week_number):
        
        filteredHolidays = []
        for i in range(len(h1.innerHolidays)):
            if h1.innerHolidays[i].date.isocalendar().week == week_number and h1.innerHolidays[i].year == year:
                filteredHolidays.append(h1.innerHolidays[i])
                
        return filteredHolidays
        
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays


    def displayHolidaysInWeek(holidayList):
        
        for i in range(len(holidayList)):
            print(str(holidayList[i]))
        
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
    

#     def getWeather(weekNum):
#         # Convert weekNum to range between two days
#         # Use Try / Except to catch problems
#         # Query API for weather in that week range
#         # Format weather information and return weather string.
#         pass

    def viewCurrentWeek():
        currentWeek = now.date.isocalendar().week
        return int(currentWeek)
         
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results


### Helper Functions 

def holidayInSystem(holidayInput):
    tmp_list = []
    
    for i in range(len(holiday_list)):
        if str(holiday_list[i].name) == holidayInput:
            tmp_list.append(holiday_list[i].name)
    
    if len(tmp_list) > 0:
        print("Holiday in system.")
        return False
    else:
        print("Holiday not in system. Please input a different holiday.")
        return True
    
    
def dateInRange(dateInput):
    try:
        dateInput = int(dateInput)
        
    except:
        print("Error: Please enter a number year")
        return True
        
    if dateInput not in [2020, 2021, 2022, 2023, 2024]:
        print("Sorry, year entered is out of range.")
        return True
    else:
        return False
    


h1 = HolidayList() 
lastSavedState = str(h1.innerHolidays)

def main():
    global h1
    global lastSavedState
    __name__ = "__main__"
#     loggedIn = True
#     while loggedIn == True: 
        
    HoliCount = HolidayList.numHolidays(h1)

    print("Welcome to Holiday Management System")
    print("======================")
    print(f"There are currently {HoliCount} holidays stored in the system.")

    print("Holiday Menu")
    print("======================")
    print(" 1. Add a Holiday \n 2. Remove a Holiday\n 3. Save Holiday List\n 4. View Holidays\n 5. Exit")

    correctInput = False
    while not correctInput:
        userInput = input("Please enter a number between 1 and 5 to navigate... ")
        try: 
            menuNav = int(userInput)
            if menuNav > 0 and menuNav < 6: 
                correctInput = True
            else:
                print("Error: Input not in range.")
                correctInput = False
        except: 
            print("Error: Input not a number.")
            correctInput = False

    if menuNav == 1: 
        ## Ask user what holiday they want to add
        stillMenu1_name = True
        while stillMenu1_name == True:
            holiday_name_input = capwords(input("what is the name of the holiday?  "))
            stillMenu1_name = holidayInSystem(holiday_name_input)

        ## Ask user for what year
        stillMenu1_date = True
        while stillMenu1_date == True:
            holiday_date_input = input(f"For what year (between 2020-2024) would you like to add {holiday_name_input}?  ")
            stillMenu1_date = dateInRange(holiday_date_input)


        for i in range(len(holiday_list)):
            if str(holiday_list[i].name) == holiday_name_input and holiday_list[i].year == int(holiday_date_input):
                HolidayList.addHoliday(h1, holiday_list[i])
                stillMenu1_date = False



    elif menuNav == 2:
        stillMenu2 = True
        while stillMenu2:
            holiday_name_input = capwords(input("what is the name of the holiday you want to remove?  "))
            tmp_list = h1.findHoliday(holiday_name_input)
            if len(tmp_list) < 1:
                stillMenu2 = True
                print(f"Error: {holiday_name_input} not found.")
            else:
                tmp_year_list = [x.year for x in tmp_list]

                print(f"{holiday_name_input} found for the year(s): {tmp_year_list}.")

                stillMenu2_year = True
                while stillMenu2_year:
                    removal_year = int(input(f"For which year would you like to remove {holiday_name_input}?  "))
                    stillMenu2_year = dateInRange(removal_year)

                HolidayList.removeHoliday(h1, holiday_name_input, removal_year)
                stillMenu2 = False

    elif menuNav == 3:
        toSave = (input("Are you sure you want to save your changes? y/n... ")).upper()

        badInput = True
        while badInput:
            if toSave == "Y":
                badInput = False
                lastSavedState = str(h1.innerHolidays)
                fn = input("Enter name for export file:  ")
                HolidayList.save_to_json(fn)
            elif toSave == "N":
                print("File save cancelled.")
                badInput = False
            else:
                print("Please input 'y' for yes or 'n' for no.")
                badInput = True


    elif menuNav == 4:
        viewYear = int(input("Which year?  "))
        viewWeek = input("Which week? Leave blank for current week.  ")
        if viewWeek == '':
            viewWeek = HolidayList.viewCurrentWeek

        try:
            viewWeek = int(viewWeek)
        except:
            print("Error. Please enter a number for week.")

        viewList = HolidayList.filter_holidays_by_week(viewYear, viewWeek)

        if len(viewList) < 1: 
            print(f"You have no saved holidays in week {viewWeek} of {viewYear}.")
        else:
            print(f"These are the holiday(s) for week {viewWeek} of {viewYear}:")
            HolidayList.displayHolidaysInWeek(viewList)


    else:

        stillSaving = True
        while stillSaving == True:  
            if str(h1.innerHolidays) == lastSavedState:
                toExit = (input("Are you sure you want to exit? y/n.. ")).upper()
            else:
                toExit = (input("Are you sure you want to exit? All unsaved changes will be lost! y/n.. ")).upper()

            if toExit == 'Y':
                stillSaving = False
                print("Goodbye!")
                __name__ = "not"
            elif toExit == 'N':
                stillSaving = False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                stillSaving = True


#             loggedIn = False
#             __name__ = "not"



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


    if __name__ == "__main__":
        main();



main()


