import PhoneBookModule
import PhoneBookEditor
import os
import time


usersPhoneBook = open("Phone_Book.txt", 'r', encoding="utf8")
toParse = usersPhoneBook.read()
usersPhoneBook.close()

currentPhoneBook = []
lenOfBook = PhoneBookEditor.parseToClassObj(toParse, -1, currentPhoneBook)

#for record in currentPhoneBook:
#    print(record)

notQuitProgram = True
lightBlueTheme = "\033[36m"
whiteTheme = "\033[37m"
message = "\033[37mFollow all the instructions below, but in case if you want\n" \
          "interrupt the record creation and quit - press * (this record would not be saved)\n"

while notQuitProgram:
    print("--Welcome to the Top-Level Phone Book Manager--\n",
          "1. View all records in current book\n",
          "2. Add a new record to the book\n",
          "3. Edit a record\n",
          "4. Delete a record\n",
          "5. Quick browse in records\n",
          "6. Show the age of a person\n",
          "7. Show the records with the nearest birthdays\n",
          "8. Help\n",
          "9. Quit\n",
          ">>>", end="")
    notQuitProgram = input()
    if notQuitProgram == "1":
        os.system("cls")
        for record in currentPhoneBook:
            print(record)
        os.system("cls")
    elif notQuitProgram == "2":
        while True:
            os.system("cls")
            print(message, sep="")
            newName = PhoneBookEditor.editNames("new name")
            os.system("cls")
            if not newName:
                break
            print(message, sep="")
            newSurname = PhoneBookEditor.editNames("new surname")
            os.system("cls")
            if not newSurname:
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
            newNumbers, settings = PhoneBookEditor.editNumbers(False)
            os.system("cls")
            if not newNumbers:
                break
            print(message, sep="")
            newName, newSurname, newBirthdate, newNumbers, settings = \
                PhoneBookEditor.editsCommandCenter(newName, newSurname, newBirthdate, newNumbers, settings)
            newField = newName + ' ' + newSurname + ' ' + newBirthdate
            lenOfBook = PhoneBookEditor.parseToClassObj(newField, lenOfBook, currentPhoneBook)
            print(whiteTheme, end="")
            os.system("cls")
            break
    elif notQuitProgram == "3":
        os.system("cls")
        print(message)
        print("First, search for record to edit it\n")
    elif notQuitProgram == "9":
        os.system("cls")
        break
    else:
        print(" Error! No such command in list. Please, try again")
        time.sleep(2)
        os.system("cls")

for record in currentPhoneBook:
    print(record)