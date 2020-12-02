import datetime

lightBlueTheme = "\033[36m"
whiteTheme = "\033[37m"

class NumberTypes:
    def __init__(self):
        self.mobiles = set()
        self.workNums = set()
        self.homeNums = set()

    def writeByTypes(self, phoneNums, settings):
        for i in range(len(phoneNums)):
            if settings[i].lower() == 'm':
                self.mobiles.add(phoneNums[i])
            elif settings[i].lower() == 'w':
                self.workNums.add(phoneNums[i])
            elif settings[i].lower() == 'h':
                self.homeNums.add(phoneNums[i])

    def __str__(self):
        catalogue = ""
        if self.mobiles:
            catalogue = "\033[36m\nMobile numbers:\033[37m\n"
            for number in self.mobiles:
                catalogue = catalogue + number + '\n'
        if self.workNums:
            catalogue = catalogue + "\033[36m\nWork numbers:\033[37m\n"
            for number in self.workNums:
                catalogue = catalogue + number + '\n'
        if self.homeNums:
            catalogue = catalogue + "\033[36m\nHome numbers:\033[37m\n"
            for number in self.homeNums:
                catalogue = catalogue + number + '\n'
        return catalogue


class PhoneBook:
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.phNumbers = NumberTypes()
        self.birthdate = ""

    def __str__(self):
        return "%s %s %s %s" % (self.name, self.surname, self.birthdate, self.phNumbers)

    def countAge(self, inStr):
        if self.birthdate:
            today = datetime.date.today()
            age = today.year - int(self.birthdate[6:]) - \
                      ( (today.month + today.day) < ( int(self.birthdate[3:5]) + int(self.birthdate[:2]) ) )
            if inStr:
                message = self.name + ' ' + self.surname + "'s age is " + str(age)
                return message
            else:
                return age
        elif not inStr:
            return False
        else:
            return " \033[37mImpossible to get the age - birthdate field is not filled"
