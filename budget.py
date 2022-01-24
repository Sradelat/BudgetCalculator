class Category:

    def __init__(self, category):
        self.category = category.center(30, "*")  # required formatting
        self.ledger = []
        self.entry = {}
        self.bal = 0  # running balance per object
        self.cattrans = str(category)  # prints string attached to object - used for transfer function
        self.totspent = 0  # running total spent in a category

    def deposit(self, amount, description=""):  # adds to the object's balance
        self.ledger.append({"amount": amount, "description": description})
        self.bal = self.bal + amount

    def withdraw(self, amount, description=""):  # withdraws from objects balance - checks to see if funds first
        funds = self.check_funds(amount)
        self.totspent = self.totspent + amount
        if not funds:
            withdraw = False
        else:
            self.bal = self.bal - amount
            amount = 0 - amount
            self.ledger.append({"amount": amount, "description": description})
            withdraw = True
        return withdraw

    def withtot(self):  # withdrawal totals for each object
        return self.totspent

    def get_balance(self):  # returns the current running balance
        return self.bal

    def transfer(self, amount, to):  # checks for available funds to transfer then commits from one object to another
        funds = self.check_funds(amount)
        if not funds:
            transfer = False
        else:
            to.ledger.append({"amount": amount, "description": "Transfer from " + self.cattrans})
            transamount = 0 - amount  # flip to a negative for ease of use
            self.ledger.append({"amount": transamount, "description": "Transfer to " + to.cattrans})
            self.bal += transamount  # update current object balance
            to.bal += amount  # update balance transferred to other object
            transfer = True
        return transfer

    def check_funds(self, amount):  # used for withdrawals
        funds = self.bal - amount
        if funds < 0:
            return False
        else:
            return True

    def __str__(self):  # used when an object is called by name
        call = str(self.category)  # call returns the string entered with the object + formatting needed
        for self.entry in self.ledger:
            dcall = "{:.2f}".format(self.entry["amount"])  # gives each entry 2 dec points
            calldes = self.entry["description"]
            call = call + "\n" + calldes[:23].ljust(23) + dcall[:7].rjust(7)  # formatting
        totcall = call + "\n" + "Total: " + str(self.bal)  # formatted entries + end total
        return totcall


def total_spent(categories):  # for graph use
    totlst = []  # withdrawal totals
    stotal = 0  # sum of totals
    perclst = []
    for cat in categories:
        ctotal = "{:.2f}".format(cat.withtot())  # cat total
        totlst.append(ctotal)  # storing for next loop
        stotal = stotal + float(ctotal)  # sum of all totals
    for total in totlst:
        perc = float(total) / stotal  # calculate percent
        round_perc = round(perc, 2) * 100  # rounding off but not up to next 10
        perclst.append(round_perc)  # for graph use

    return perclst


def create_spend_chart(categories):
    graph = [
        "100| ",
        " 90| ",
        " 80| ",
        " 70| ",
        " 60| ",
        " 50| ",
        " 40| ",
        " 30| ",
        " 20| ",
        " 10| ",
        "  0| ",
    ]

    perclst = total_spent(categories)  # populate list
    for perc in perclst:
        y = 110  # y-axis
        i = -1  # index of graph list
        for line in graph:
            y = y - 10  # increment y
            i = i + 1  # increment index
            if perc >= y:
                graph[i] = graph[i] + "o  "  # populate if true
            else:
                graph[i] = graph[i] + "   "  # empty space if not

    catlst = []  # stores object strings
    mnum = 0  # stores length of longest word
    dashes = "    -"

    for category in categories:
        catlst.append(category.cattrans)  # adding each category to a list for ease of use
        dashes = dashes + "---"  # create dash line per cat

    for entry in catlst:      # maxcat = max(catlst, key=len)  can be shortened with this
        lnum = len(entry)
        if lnum > mnum:  # finding the longest word in the list
            mnum = lnum

    x = ""  # x-axis
    for length in range(mnum):  # iterating for every letter in the longest word
        feed = "     "  # first indent in line
        for cat in catlst:
            if length >= len(cat):  # if # of iterations is higher than word length -> do something
                feed = feed + "   "
            else:
                feed = feed + cat[length] + "  "  # word indexed by number of iterations
        feed = feed + "\n"
        x = x + feed  # bringing it all together

    create_graph = "Percentage spent by category\n"  # bring it all together
    for line in graph:
        create_graph += line + "\n"
    create_graph += dashes + "\n"
    create_graph += x.rstrip("\n")  # .rstrip for very specific formatting test

    return create_graph
