import PhoneBookModule
import PhoneBookEditor
import os
import time


os.system("cls")
usersPhoneBook = open("Phone_Book.txt", 'r', encoding="utf8")
toParse = usersPhoneBook.read()
usersPhoneBook.close()

currentPhoneBook = []
lenOfBook = PhoneBookEditor.parseToClassObj(toParse, -1, currentPhoneBook)

notQuitProgram = True
lightBlueTheme = "\033[36m"
whiteTheme = "\033[37m"
message = "\033[37mFollow all the instructions below, but in case if you want\n" \
          "interrupt the action and quit - press * (all changes would not be saved)\n"

while notQuitProgram:
    print("--Welcome to the Top-Level Phone Book Manager--\n",
          "1. View all records in current book\n",
          "2. Add a new record to the book\n",
          "3. Edit a record\n",
          "4. Delete a record\n",
          "5. Quick browse in records\n",
          "6. Show the age of a person\n",
          "7. Show the records with the nearest birthdays\n",
          "8. Find by age\n",
          "9. Quit\n",
          ">>>", end="")
    notQuitProgram = input()
    if notQuitProgram == "1":
        os.system("cls")
        for (i, record) in enumerate(currentPhoneBook):
            print(whiteTheme, i + 1, '.', ' ', record, sep="")
        print(" Print anything to quit to main menu")
        print(lightBlueTheme, ">>>", end="")
        quitCom = input()
        print(whiteTheme)
        os.system("cls")
    elif notQuitProgram == "2":
        os.system("cls")
        while True:
            tries = True
            quitCom = False
            while tries:
                print(message, sep="")
                newName = PhoneBookEditor.editNames("new name")
                os.system("cls")
                if not newName:
                    quitCom = True
                    break
                print(message, sep="")
                newSurname = PhoneBookEditor.editNames("new surname")
                if not newSurname:
                    quitCom = True
                    break
                indexes = list(range(lenOfBook + 1))
                isUnique = PhoneBookEditor.browseRecords(newName, "ns", currentPhoneBook, indexes, newSurname)
                if isUnique != -1:
                    print(whiteTheme, "Error! The name+surname is a unique identifier!\n",
                          "Entered name+surname is already used in phone book\n",
                          "1. Try again\n",
                          "2. Show record with correlation in name+surname\n",
                          "3. Quit to main menu") # реализация работы с идентификатором
                    while True:
                        print(lightBlueTheme, ">>>", end="")
                        choice = input()
                        if choice == "1":
                            break
                        elif choice == "2":
                            print(whiteTheme, currentPhoneBook[isUnique], sep="")
                            print(whiteTheme, "Try to edit this first. To quit this action enter 3 or 1")
                        elif choice == "3" or choice == '*':
                            quitCom = True
                            tries = False
                            break
                        else:
                            print(whiteTheme, "Error! No such command in list. Please, try again")
                    os.system("cls")
                else:
                    break
                os.system("cls")
            if quitCom:
                break
            print(message, sep="")
            print(" Optional: enter the person's birthdate\n",
                  "(correct format: DD.MM.YYYY)\n",
                  "(if you want to miss this field - press enter)")
            newBirthdate = PhoneBookEditor.editDate(False)
            os.system("cls")
            if newBirthdate == '*':
                break
            print(message, sep="")
            newNumbers, settings = PhoneBookEditor.createNumbers(False)
            os.system("cls")
            if not newNumbers:
                break
            newNums = PhoneBookModule.NumberTypes()
            newNums.writeByTypes(newNumbers, settings)
            print(message, sep="")
            newName2, newSurname2, newBirthdate2, newNums2 = \
                PhoneBookEditor.editsCommandCenter(newName, newSurname, newBirthdate, newNums,
                                                   currentPhoneBook, lenOfBook + 1)
            if newName2:
                 newName, newSurname, newBirthdate, newNums = newName2, newSurname2, newBirthdate2, newNums2
            else:
                break
            newName = newName.replace(' ', '.')
            newSurname = newSurname.replace(' ', '.')
            newField = newName + ' ' + newSurname + ' ' + newBirthdate
            lenOfBook = PhoneBookEditor.parseToClassObj(newField, lenOfBook, currentPhoneBook)
            currentPhoneBook[lenOfBook].phNumbers = newNums
            print(whiteTheme)
            os.system("cls")
            break
        print(whiteTheme)
        os.system("cls")
    elif notQuitProgram == "3":
        os.system("cls")
        quitCom = 0
        while not quitCom:
            print(message)
            print("First, search for record to edit it\n")
            index = PhoneBookEditor.printNChooseRes(currentPhoneBook, "edit", lenOfBook + 1)
            os.system("cls")
            if not index == '*':

                newName2, newSurname2, newBirthdate2, newNums2 = \
                PhoneBookEditor.editsCommandCenter(currentPhoneBook[index].name, currentPhoneBook[index].surname,
                                               currentPhoneBook[index].birthdate, currentPhoneBook[index].phNumbers,
                                               currentPhoneBook, lenOfBook + 1)
                if newName2:
                    currentPhoneBook[index].name, currentPhoneBook[index].surname, \
                    currentPhoneBook[index].birthdate, currentPhoneBook[index].phNumbers = \
                        newName2, newSurname2, newBirthdate2, newNums2
                    print(whiteTheme, "The record was edited\n")
                else:
                    break
            else:
                print(whiteTheme, "Edit was denied, chosen record is remained as it was\n")
            quitCom = PhoneBookEditor.mainMenuYN("edit another record", "Quit to main menu?\n")
            os.system("cls")
            print(whiteTheme)
            os.system("cls")
    elif notQuitProgram == "4":
        os.system("cls")
        quitCom = 0
        while not quitCom:
            print(message)
            print("First, search for record to delete it\n")
            index = PhoneBookEditor.printNChooseRes(currentPhoneBook, "delete", lenOfBook + 1)
            os.system("cls")
            if not index == '*':
                currentPhoneBook.pop(index)
                lenOfBook -= 1
                print(whiteTheme, "Deletion went successfully!\n")
            else:
                print(whiteTheme, "Deletion was denied, chosen record is saved\n")
            quitCom = PhoneBookEditor.mainMenuYN("delete another record", "Quit to main menu?\n")
            print(whiteTheme)
            os.system("cls")
    elif notQuitProgram == "5":
        os.system("cls")
        quitCom = 0
        while not quitCom:
            os.system("cls")
            print(message)
            indexes = PhoneBookEditor.whileInterface(currentPhoneBook, lenOfBook + 1)
            os.system("cls")
            if indexes:
                i = 1
                print(whiteTheme, "The results of search:")
                for index in indexes:
                    print(whiteTheme, i, '.', ' ', currentPhoneBook[index], sep="")
                    i += 1
                quitCom = PhoneBookEditor.mainMenuYN("search for another record", "Quit to main menu?\n")
            elif indexes == '*':
                quitCom = True
            print(whiteTheme)
            os.system("cls")
    elif notQuitProgram == "6":
        os.system("cls")
        quitCom = 0
        while not quitCom:
            print(message)
            print("First, search for record of the person, whose age you need to know\n")
            index = PhoneBookEditor.printNChooseRes(currentPhoneBook, "show the age of", lenOfBook + 1)
            os.system("cls")
            if not index == '*':
                print(whiteTheme, currentPhoneBook[index].countAge(True))
            else:
                print(whiteTheme, "The request of person's age was denied\n")
            quitCom = PhoneBookEditor.mainMenuYN("show the age for another record", "Quit to main menu?\n")
            print(whiteTheme)
            os.system("cls")
    elif notQuitProgram == "7":
        os.system("cls")
        nearBDs = PhoneBookEditor.nearestBDs(currentPhoneBook)
        if nearBDs:
            for (i, record) in enumerate(nearBDs):
                print(whiteTheme, i + 1, '.', ' ', record, sep="")
        else:
            print(" There is no birthdays in month")
        print(" Print anything to quit to main menu")
        print(lightBlueTheme, ">>>", end="")
        quitCom = input()
        print(whiteTheme)
        os.system("cls")
    elif notQuitProgram == "8":
        os.system("cls")
        quitCom = 0
        while not quitCom:
            print(message)
            print(" Enter the age")
            while True:
                print(lightBlueTheme, ">>>", end="")
                age = input()
                if -1 < int(age) < 121:
                    break
                elif age == '*':
                    quitCom = True
                    break
                else:
                    print(whiteTheme, "Error! This is incorrect age :0 Please, try again")
            if quitCom:
                break
            print(whiteTheme, "Find the persons, who are:\n",
                  "1. Younger\n",
                  "2. Elder\n",
                  "3. Equal to this age")
            needAgedPeople = []
            while True:
                print(lightBlueTheme, ">>>", end="")
                statement = input()
                age = int(age)
                if statement == "1":
                    needAgedPeople, statement = PhoneBookEditor.showAge(age, 'l', currentPhoneBook)
                    break
                elif statement == "2":
                    needAgedPeople, statement = PhoneBookEditor.showAge(age, 'm', currentPhoneBook)
                    break
                elif statement == "3":
                    needAgedPeople, statement = PhoneBookEditor.showAge(age, 'e', currentPhoneBook)
                    break
                elif statement == '*':
                    quitCom = True
                    break
                else:
                    print(whiteTheme, "Error! No such command in list. Please, try again")
            if quitCom:
                break
            if needAgedPeople:
                print(whiteTheme, "Search results (people, who are", statement, age, "years):")
                for index in needAgedPeople:
                    print(whiteTheme, currentPhoneBook[index].name, currentPhoneBook[index].surname, '-',
                          currentPhoneBook[index].countAge(False), "years")
            else:
                print(" There was not found matches by these criteria")
            quitCom = PhoneBookEditor.mainMenuYN("find another people by age", "Quit to main menu?\n")
            print(whiteTheme)
            os.system("cls")
        print(whiteTheme)
        os.system("cls")
    elif notQuitProgram == "9":
        print(whiteTheme)
        os.system("cls")
        break
    else:
        print(" Error! No such command in list. Please, try again")
        time.sleep(2)
        os.system("cls")

usersPhoneBook = open("Phone_Book.txt", 'w', encoding="utf8")
PhoneBookEditor.writeToFile(currentPhoneBook, usersPhoneBook)
usersPhoneBook.close()
