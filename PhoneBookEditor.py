import PhoneBookModule
import time
import os
import re
import datetime
import calendar


# ☆¯'*´*•.,☆,.•*’*´¯☆   ~Function to parse data from the file~   ☆¯'*´*•.,☆,.•*’*´¯☆
def parseToClassObj(toParse, index, currentPhoneBook):
    if toParse:
        toParse = toParse.split('\n')
        phoneT = ''
        phoneNums = []
        settings = []
        for part in toParse:
            if part.isnumeric():
                phoneNums.append(part)
                settings.append(phoneT)
            elif not (':' in part) and part:
                if phoneNums:
                    currentPhoneBook[index].phNumbers.writeByTypes(phoneNums, settings)
                    phoneNums = []
                    settings = []
                index += 1
                currentPhoneBook.append(PhoneBookModule.PhoneBook())
                part = part.split()
                currentPhoneBook[index].name = part[0].replace('.', ' ')
                currentPhoneBook[index].surname = part[1].replace('.', ' ')
                if len(part) > 2:
                    currentPhoneBook[index].birthdate = part[2]
            elif part:
                if part[0] == 'M':
                    phoneT = 'm'
                elif part[0] == 'W':
                    phoneT = 'w'
                elif part[0] == 'H':
                    phoneT = 'h'
    currentPhoneBook[index].phNumbers.writeByTypes(phoneNums, settings)
    return index


def writeToFile(currentPhoneBook, file):
    for record in currentPhoneBook:
        namestr = record.name.replace(' ', '.') + ' ' + record.surname.replace(' ', '.') + \
            ' ' + record.birthdate
        phString = ""
        if record.phNumbers.mobiles:
            phString = "\nMobile phones:\n"
            phString += '\n'.join(record.phNumbers.mobiles)
            phString += '\n'
        if record.phNumbers.workNums:
            phString += "\nWork phones:\n"
            phString += '\n'.join(record.phNumbers.workNums)
            phString += '\n'
        if record.phNumbers.homeNums:
            phString += "\nHome phones:\n"
            phString += '\n'.join(record.phNumbers.homeNums)
            phString += '\n'
        namestr += phString
        file.write(namestr)


def editNames(message):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    print(whiteTheme, "Enter the person's", message, "(latin, numbers and spacebars only)", lightBlueTheme, "\n",
          ">>>", end="")
    newName = input()
    if newName == '*':
        return False
    passed = False
    toCheck = []
    while not passed:
        passed = True
        toCheck = newName.split()
        for word in toCheck:
            if not (word.isalnum()) or word[0] < "A":
                print(whiteTheme, "Error! Incorrect format for the ", message, "! Please, try again\n",
                      " Make sure it doesn't start with a number or has no illegal symbols in it\n",
                      lightBlueTheme, ">>>", end="", sep="")
                newName = input()
                if newName == '*':
                    return False
                passed = False
                break
    newName = ""
    for i in range(len(toCheck)):
        toCheck[i] = toCheck[i].capitalize()
    newName = ' '.join(toCheck)
    return newName


def editDate(question):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    if question:
        print(whiteTheme, "Enter the person's birthdate\n",
              "(correct format: DD.MM.YYYY)")
    print(lightBlueTheme, ">>>", end="")
    newBirthdate = input()
    if newBirthdate == '*':
        return False
    passed = checkData(newBirthdate)
    while not (passed or newBirthdate == ""):
        print(whiteTheme, "Error! Incorrect format of the date! Please, try again\n",
              "Make sure it doesn't contain any other symbols except numbers and commas\n",
              "Remember that correct format is DD.MM.YYYY", lightBlueTheme, "\n",
              ">>>", end="")
        newBirthdate = input()
        if newBirthdate == '*':
            return newBirthdate
        passed = checkData(newBirthdate)
    return newBirthdate


def checkData(date):
    try:
        time.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def createNumbers(edit):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    print(whiteTheme, "Enter one phone number, then press enter\n",
          "Number format: only numbers, 11 symbols in total")
    newNumbers = []
    settings = []
    oneMore = True
    while oneMore:
        print(lightBlueTheme, ">>>", end="")
        newNumber = input()
        if newNumber == '*':
            return [], []
        if newNumber[0] == '+' and newNumber[1] == '7':
            newNumber = '8' + newNumber[2:]
        while not (newNumber.isnumeric()) or (len(newNumber) != 11):
            print(whiteTheme, "Error! Incorrect format of the phone number! Please, try again\n",
                  "Make sure it doesn't contain any letters or other illegal symbols in it\n",
                  "Remember that correct number is 11 numbers long", lightBlueTheme, "\n",
                  ">>>", end="")
            newNumber = input()
            if newNumber == '*':
                return [], []
            if newNumber[0] == '+' and newNumber[1] == '7':
                newNumber = '8' + newNumber[2:]
        newNumbers.append(newNumber)
        if not edit:
            print(whiteTheme, "Choose the category for entered number:\n",
                  "1. Mobile\n",
                  "2. Work\n",
                  "3. Home")
            while True:
                print(lightBlueTheme, ">>>", end="")
                category = input()
                if category == '1':
                    settings.append('m')
                    break
                elif category == '2':
                    settings.append('w')
                    break
                elif category == '3':
                    settings.append('h')
                    break
                elif category == '*':
                    return [], []
                else:
                    print(whiteTheme, "Error! No such category in supported. Please, try again")
            print(whiteTheme, "Do you want to add one more number?\n",
                  "1. No\n",
                  "2. Yes")
            while True:
                print(lightBlueTheme, ">>>", end="")
                oneMore = input()
                if oneMore == "1":
                    oneMore = False
                    break
                elif oneMore == "2":
                    break
                elif oneMore == '*':
                    return [], []
                else:
                    print(whiteTheme, "Error! No such command in list. Please, try again")
        else:
            return newNumbers[0]
    return newNumbers, settings


def editClassObjNums(nums):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    os.system("cls")
    edit = True
    mobiles = list(nums.mobiles)
    works = list(nums.workNums)
    homes = list(nums.homeNums)
    phoneNums = []
    settings = []
    lastChange = ""
    while edit:
        if lastChange:
            print(lastChange)
        i = 1
        print(whiteTheme, "Current catalogue:\n",
              "(don't worry, the actual record would not be edited before you confirm all edits\n")
        if mobiles:
            print(lightBlueTheme, "Mobile numbers:")
            for number in mobiles:
                print(whiteTheme, ' ', i, '.', ' ', number, sep='')
                i += 1
            print("")
        if works:
            print(lightBlueTheme, "Work numbers:")
            for number in works:
                print(whiteTheme, ' ', i, '.', ' ', number, sep='')
                i += 1
            print("")
        if homes:
            print(lightBlueTheme, "Home numbers:")
            for number in homes:
                print(whiteTheme, ' ', i, '.', ' ', number, sep='')
                i += 1
            print("")
        print('\n', whiteTheme, "Choose the option:\n",
              "1. Edit phone number\n",
              "2. Delete phone number\n",
              "3. Add new phone number\n",
              "4. Confirm and back to edits menu")
        while True:
            print(lightBlueTheme, ">>>", end="")
            edit = input()
            if edit == '1':
                index, category = chooseNumber(i, "edit", len(mobiles), len(works), len(homes))
                if index == '*':
                    return False
                newNum = createNumbers(True)
                if not newNum:
                    return False
                if category == 'm':
                    mobiles[index] = newNum
                elif category == 'w':
                    works[index] = newNum
                elif category == 'h':
                    homes[index] = newNum
                break
            elif edit == '2':
                if not (len(mobiles) + len(works) + len(homes)) < 2:
                    index, category = chooseNumber(i, "delete", len(mobiles), len(works), len(homes))
                    if index == '*':
                        return False
                    if category == 'm':
                        mobiles.pop(index)
                    elif category == 'w':
                        works.pop(index)
                    elif category == 'h':
                        homes.pop(index)
                else:
                    print(whiteTheme, "Error! You can't leave the numbers field absolutely empty\n",
                          "If you don't want this number in record, just edit it")
                    time.sleep(3)
                break
            elif edit == '3':
                phoneNums, settings = createNumbers(False)
                if not phoneNums:
                    return False
                for (i, category) in enumerate(settings):
                    if category == 'm':
                        mobiles.append(phoneNums[i])
                    elif category == 'w':
                        works.append(phoneNums[i])
                    elif category == 'h':
                        homes.append(phoneNums[i])
                phoneNums = settings = []
                break
            elif edit == '4':
                phoneNums = mobiles + works + homes
                for i in range(len(mobiles)):
                    settings.append('m')
                for i in range(len(works)):
                    settings.append('w')
                for i in range(len(homes)):
                    settings.append('h')
                newNumCatalogue = PhoneBookModule.NumberTypes()
                newNumCatalogue.writeByTypes(phoneNums, settings)
                return newNumCatalogue
            elif edit == '*':
                os.system("cls")
                return False
            else:
                print(whiteTheme, "Error! No such command in list. Please, try again")
        os.system("cls")
    os.system("cls")


def chooseNumber(i, message, mlen, wlen, hlen):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    print(whiteTheme, "Now, choose the number to", message)
    while True:
        print(lightBlueTheme, ">>>", end="")
        index = input()
        if 0 < int(index) < i:
            index = int(index)
            if index <= mlen:
                index = int(index) - 1
                return index, 'm'
            elif index <= mlen + wlen:
                index = int(index) - mlen - 1
                return index, 'w'
            elif index <= mlen + wlen + hlen:
                index = int(index) - mlen - wlen - 1
                return index, 'h'
        elif index == '*':
            return index
        else:
            print(whiteTheme, "Error! List index out of range!\n",
                  "Please, try again")


# ☆¯'*´*•.,☆,.•*’*´¯☆ This function does not change the actual records,
# but prepares new fields for rerecord ☆¯'*´*•.,☆,.•*’*´¯☆
# interface
def editsCommandCenter(name="", surname="", birthdate="", phNums=""):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    edit = True
    while edit:
        print(whiteTheme, "The current record is", lightBlueTheme, "\n\n",
              name + ' ' + surname + ' ' + birthdate)
        print(phNums)
        print(whiteTheme, "Do you want to confirm all data?\n",
              "If you want to edit any field, choose one of the options below\n",
              "(to interrupt the editing - press * (all changes would not be saved)\n\n",
              "1. Confirm and quit\n",
              "2. Edit name\n",
              "3. Edit surname\n",
              "4. Edit birthdate\n",
              "5. Edit numbers\n")
        while True:
            print(lightBlueTheme, ">>>", end="")
            edit = input()
            if edit == '1':
                edit = False
                break
            elif edit == '2':
                name = editNames("name")
                if not name:
                    return False
                break
            elif edit == '3':
                surname = editNames("surname")
                if not surname:
                    return False
                break
            elif edit == '4':
                birthdate = editDate(True)
                if birthdate == '*':
                    return birthdate
                break
            elif edit == '5':
                phNums = editClassObjNums(phNums)
                if not phNums:
                    return False
                break
            elif edit == '*':
                os.system("cls")
                return False
            else:
                print(whiteTheme, "Error! No such command in list. Please, try again")
        os.system("cls")

    return name, surname, birthdate, phNums


def browseRecords(toSearch, field, currentPhoneBook, indexesForList, toSearch2=""):
    indexes = []
    if field == 'n':
        for i in indexesForList:
            if toSearch in currentPhoneBook[i].name:
                indexes.append(i)
    elif field == 's':
        for i in indexesForList:
            if toSearch in currentPhoneBook[i].surname:
                indexes.append(i)
    elif field == 'ns':
        for i in indexesForList:
            if toSearch == currentPhoneBook[i].name and toSearch2 == currentPhoneBook[i].surname:
                return i
        return -1
    elif field == 'd':
        for i in indexesForList:
            if toSearch in currentPhoneBook[i].birthdate:
                indexes.append(i)
    elif field == 'pn':
        indexes = set()
        for i in indexesForList:
            for j in currentPhoneBook[i].phNumbers.mobiles:
                if toSearch in j:
                    indexes.add(i)
            for j in currentPhoneBook[i].phNumbers.workNums:
                if toSearch in j:
                    indexes.add(i)
            for j in currentPhoneBook[i].phNumbers.homeNums:
                if toSearch in j:
                    indexes.add(i)

    return indexes


# interface
def whileInterface(currentPhoneBook, lenOfBook):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    while True:
        print(whiteTheme, "Choose the field for search\n",
              "(if you want search for multiple fields simultaneously, enter the numbers via spacebar)\n")
        print(whiteTheme, "1. Name\n",
              "2. Surname\n",
              "3. Birthdate\n",
              "(caution: You can't search the record by the fragment of date, only full-format)\n",
              "4. Numbers (caution: 1 number per search)\n",
              "5. Quit to main menu")
        while True:
            print(lightBlueTheme, ">>>", end="")
            answer = input()
            if re.match('^[12345* ]+$', answer):
                if "5" in answer or '*' in answer:
                    return
                theOrder = answer.split()
                theOrder = set(theOrder)
                break
            else:
                print(whiteTheme, "Error! Some commands in the list are illegal!\n",
                      "Please, try again and be careful")
        indexes = list(range(lenOfBook))
        while theOrder:
            field = theOrder.pop()
            if field == '1':
                name = editNames("name")
                if not name:
                    return False
                indexes = browseRecords(name, "n", currentPhoneBook, indexes)
            elif field == '2':
                surname = editNames("surname")
                if not surname:
                    return False
                indexes = browseRecords(surname, "s", currentPhoneBook, indexes)
            elif field == '3':
                birthdate = editDate(True)
                if birthdate == '*':
                    return birthdate
                indexes = browseRecords(birthdate, "d", currentPhoneBook, indexes)
            elif field == '4':
                nums = createNumbers(True)
                if not nums:
                    return False
                indexes = browseRecords(nums, "pn", currentPhoneBook, indexes)
        if indexes:
            return indexes
        else:
            print(whiteTheme, "There was not found records, that meet the conditions of search")
            if not (mainMenuYN("quit to main menu", "Would you like to try again?\n")):
                return []


# interface
def printNChooseRes(currentPhoneBook, message, lenOfBook):
    lightBlueTheme = "\033[36m"
    whiteTheme = "\033[37m"
    indexes = whileInterface(currentPhoneBook, lenOfBook)
    if indexes:
        print(whiteTheme, "The results of search:")
        i = 1
        for index in indexes:
            print(whiteTheme, i, '.', ' ', currentPhoneBook[index], sep="")
            i += 1
        print(whiteTheme, "Choose the record to", message)
        print(lightBlueTheme, ">>>", end="")
        i = input()
        if i == '*':
            return i
        i = int(i) - 1
        if i >= len(indexes) or i < 0:
            print(whiteTheme, "Error! List index out of range!\n",
                  "Please, try again")
        else:
            print('\n', whiteTheme, currentPhoneBook[indexes[i]], sep='')
            print(whiteTheme, "You are about to", message, "this record. Confirm?\n",
                  "1. No (nothing would happen to this record)\n",
                  "2. Yes")
            while True:
                print(lightBlueTheme, ">>>", end="")
                confirm = input()
                if confirm == "1" or confirm == '*':
                    return '*'
                elif confirm == "2":
                    return indexes[i]
                else:
                    print(whiteTheme, "Error! No such command in list. Please, try again")
    else:
        return '*'


# interface
def mainMenuYN(message, message2):
    lightBlueTheme = "\033[36m"
    whiteTheme = "\033[37m"
    print(whiteTheme, message2,
          "1. Yes\n",
          "2. No,", message)
    while True:
        print(lightBlueTheme, ">>>", end="")
        quitCom = input()
        if quitCom == "1" or quitCom == '*':
            return True
        elif quitCom == "2":
            return False
        else:
            print(whiteTheme, "Error! No such command in list. Please, try again")


def nearestBDs(currentPhoneBook):
    nearBDs = []
    evenMonths = (4, 6, 9, 11)
    oddMonths = (1, 3, 5, 7, 8, 10, 12)
    february = 2
    today = datetime.date.today()
    diff = 0
    days = 1
    day = 0
    months = [int(today.month)]
    if not int(today.month) == february:
        if int(today.month) in evenMonths:
            diff = 1
            days = 30
        elif int(today.month) in oddMonths:
            diff = 2
            days = 31
        day = (days + (int(today.day) - diff)) % days
        if day == 0:
            day = days
        if day < int(today.day):
            months = [int(today.month), (int(today.month) % 12) + 1]
    else:
        if calendar.isleap(today.year):
            day = int(today.day)
        else:
            day = int(today.day) + 1
        months = [int(today.month), int(today.month) + 1]
    for record in currentPhoneBook:
        BDmonth = int(record.birthdate[3:5])
        Bday = int(record.birthdate[:2])
        if BDmonth == months[0] and int(today.day) <= Bday <= day:
            nearBDs.append(record)
        elif len(months)>1 and BDmonth == months[1] and Bday <= day:
            nearBDs.append(record)
    return nearBDs


def showAge(age, statement, currentPhoneBook):
    less = []
    equal = []
    more = []
    for (i, record) in enumerate(currentPhoneBook):
        currentAge = record.countAge(False)
        if currentAge and currentAge < age:
            less.append(i)
        elif currentAge and currentAge == age:
            equal.append(i)
        elif currentAge and currentAge > age:
            more.append(i)
    if statement == "l":
        return less, "younger than"
    elif statement == "e":
        return equal, "equal to"
    elif statement == "m":
        return more, "elder than"
