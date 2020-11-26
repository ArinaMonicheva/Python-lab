import PhoneBookModule
import time
import os


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
            elif not (':' in part):
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
            else:
                if part[0] == 'M':
                    phoneT = 'm'
                elif part[0] == 'W':
                    phoneT = 'w'
                elif part[0] == 'H':
                    phoneT = 'h'
    currentPhoneBook[index].phNumbers.writeByTypes(phoneNums, settings)
    return index


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
        print(whiteTheme, "Enter the person's new birthdate\n",
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


def editNumbers(onlyOneField):
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
        if not onlyOneField:
            print(whiteTheme, "Do you want to add one more number?\n",
                  "1. No\n",
                  "2. Yes")
            while True:
                print(lightBlueTheme, ">>>", end="")
                oneMore = input()
                if oneMore == "1":
                    oneMore = False
                    break
                elif oneMore == '*':
                    return [], []
                elif not (oneMore == "2"):
                    print(whiteTheme, "Error! No such command in list. Please, try again")
        else:
            break
    return newNumbers, settings


# ☆¯'*´*•.,☆,.•*’*´¯☆ This function does not change the actual records,
# but prepares new fields for rerecord ☆¯'*´*•.,☆,.•*’*´¯☆
def editsCommandCenter(name="", surname="", birthdate="", nums="", setts=""):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    edit = True
    while edit:
        print(whiteTheme, "The current record is", lightBlueTheme, "\n\n",
              name + ' ' + surname + ' ' + birthdate)
        print("")
        for i in range(len(nums)):
            print('', nums[i], "is", setts[i])
        print("")
        print(whiteTheme, "Where 'm' - Mobile, 'w' - Work, 'h' - Home numbers\n")
        print(" Do you want to confirm all data?\n",
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
                birthdate = editDate("surname")
                if birthdate == '*':
                    return birthdate
                break
            elif edit == '5':
                nums, setts = editNumbers(False)
                if not nums:
                    return False
                break
            elif edit == '*':
                os.system("cls")
                return False
            else:
                print(whiteTheme, "Error! No such command in list. Please, try again")
        os.system("cls")

    return name, surname, birthdate, nums, setts


def browseRecords(toSearch, toSearch2, field, lenOfBook, currentPhoneBook):
    returnRecord = []
    if field == 'n':
        for i in range(lenOfBook):
            if currentPhoneBook[i].name == toSearch:
                returnRecord.append(currentPhoneBook[i])
    elif field == 's':
        for i in range(lenOfBook):
            if currentPhoneBook[i].surname == toSearch:
                returnRecord.append(currentPhoneBook[i])
    elif field == 'ns':
        for i in range(lenOfBook):
            if currentPhoneBook[i].name == toSearch and currentPhoneBook[i].surname == toSearch2:
                returnRecord.append(currentPhoneBook[i])
    elif field == 'd':
        for i in range(lenOfBook):
            if currentPhoneBook[i].birthdate == toSearch:
                returnRecord.append(currentPhoneBook[i])
    elif field == 'pn':
        for i in range(lenOfBook):
            for j in currentPhoneBook[i].phNumbers.mobiles:
                if j == toSearch:
                    returnRecord.append(currentPhoneBook[i])
            for j in currentPhoneBook[i].phNumbers.workNums:
                if j == toSearch:
                    returnRecord.append(currentPhoneBook[i])
            for j in currentPhoneBook[i].phNumbers.workNums:
                if j == toSearch:
                    returnRecord.append(currentPhoneBook[i])

    return returnRecord


def whileInterface(func):
    whiteTheme = "\033[37m"
    lightBlueTheme = "\033[36m"
    print(whiteTheme, "Choose the field for search")
    print(whiteTheme, "1. Name + Surname\n",
          "2. Name\n",
          "3. Surname\n",
          "4. Birthdate\n",
          "5. Numbers\n",
          "6. Quit to main menu")
    while True:
        print(lightBlueTheme, ">>>", end="")
        answer = input()
        if answer == '1':
            edit = False
            break
        elif answer == '2':
            name = editNames("name")
            if not name:
                return False
            break
        elif answer == '3':
            surname = editNames("surname")
            if not surname:
                return False
            break
        elif answer == '4':
            birthdate = editDate("surname")
            if birthdate == '*':
                return birthdate
            break
        elif answer == '5':
            nums, setts = editNumbers(False)
            if not nums:
                return False
            break