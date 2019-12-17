from tkinter import *
import datetime
from datetime import date
import calendar
import csv
import backend
import os

global Entries
Entries = {}
Events= {}

if os.path.exists('remindersData.csv') == False:           # check if file exists
    with open('remindersData.csv', 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["DATE", "NAME", "TYPE", "LENGTH"])


def frontEnd():                                           # creates the interface window
    frontEnd.counter = 1
    def createEntry():
        def exportToCSV(exportData):                   # function to write to csv file
            Events[dateVar.get()] = exportData
            print(Events)
            try:
                with open('remindersData.csv', 'a', newline = '') as file:
                        writer = csv.writer(file)
                        writer.writerow([exportData])  # export data to csv
                                                        # input coming from line 60

            except():
                print('something went wrong....')

            
        def defineLength():                        # creates window to select the length of the event
            root = Tk()
            topFrame = Frame(root)
            topFrame.pack(side = TOP)
            bottomFrame = Frame(root)
            bottomFrame.pack(side = BOTTOM) 
            contentFrame = Frame(bottomFrame)
            buttonFrame = Frame(bottomFrame)
            contentFrame.pack(side = TOP)
            buttonFrame.pack(side = BOTTOM)
            Message(topFrame,text= "Select length - \n").pack(side = TOP)
            start = Entry(contentFrame)
            end = Entry(contentFrame)
            Message(contentFrame, text = "From -").pack(side = LEFT, pady = (11,0))
            start.pack(side = LEFT)
            Message(contentFrame,text= "To -").pack(side = LEFT, pady = (0,3))
            end.pack(side = LEFT, padx = (0,5))
            Button(buttonFrame, text = "submit").pack()
            root.mainloop()

        def submit_entry():       
            if createEntry.eventLengthVar.get() == createEntry.subEventType[0]:       # if all-day event
                Entries[entry.get()] = {"Type": createEntry.eventTypeVar.get(), "Length": createEntry.eventLengthVar.get()}
            elif createEntry.eventLengthVar.get() == createEntry.subEventType[-1]:    # if limited event
                defineLength()
            createEntry.submitE.pack_forget()
            exportToCSV([dateVar.get(), entry.get(), createEntry.eventTypeVar.get(), createEntry.eventLengthVar.get()])     # fetch input of all the entries and store them to a list

    
        createEntry.evenTypes = ['Reminder', 'Event']                                              # create window for entering events
        createEntry.subEventType = ['All-Day', 'Limited']                               
        replicateFrame = Frame(rightFrame, highlightbackground = "black", highlightthickness = 2)
        labelFrame = Frame(replicateFrame)
        entryFrame = Frame(replicateFrame)
        replicateFrame.pack(side = TOP)
        labelFrame.pack(side = LEFT)
        entryFrame.pack(side = RIGHT)

        createEntry.eventTypeVar = StringVar(entryFrame)
        createEntry.eventLengthVar = StringVar(entryFrame)
        createEntry.eventTypeVar.set("Select type")
        createEntry.eventLengthVar.set("Select length")
        createEntry.eventSelector = OptionMenu(entryFrame, createEntry.eventTypeVar, *createEntry.evenTypes)
        createEntry.eventSelector.pack(side = LEFT)
        createEntry.eventLength = OptionMenu(entryFrame, createEntry.eventLengthVar, *createEntry.subEventType)
        createEntry.eventLength.pack(side = LEFT)


        Label(labelFrame, text =str("Entry #" + str(frontEnd.counter))).pack()
        entry = Entry(entryFrame)
        entry.pack(side = TOP)
        
        createEntry.submitE = Button(entryFrame, text = "SUBMIT ENTRY", command = submit_entry)
        createEntry.submitE.pack(side = TOP)
        createEntry.addEvent = Button(entryFrame, text = "ADD EVENT", command = add_entry)
        createEntry.addEvent.pack(side = TOP)

    def add_entry():                              # call the window creation function for another entry
        createEntry.addEvent.pack_forget()
        frontEnd.counter += 1
        createEntry()

 
    plannerWindow = Tk()                           # the root window
    rootFrame = Frame(plannerWindow)
    topFrame = Frame(rootFrame)
    bottomFrame = Frame(rootFrame)
    leftFrame = Frame(topFrame)
    rightFrame = Frame(topFrame)
    rootFrame.pack()
    topFrame.pack(side = TOP)
    bottomFrame.pack(side = BOTTOM)
    leftFrame.pack(side = LEFT)
    rightFrame.pack(side = RIGHT)

    todaysDate = date.today()
    curDay = int(str(date.today())[-2:])            # fetch todays date (DD)

    diff = datetime.timedelta(days = 1)             # calculate next date

    print("today is ",str(curDay))
    Message(leftFrame, text = str("today is "+ str(todaysDate)), anchor = "ne").pack(side =TOP)

    lastDay = int(calendar.monthrange(2019, 12)[1])  # get total number of days in month            
    print("days this month,", lastDay)
    remainingDays = abs(lastDay - curDay)
    print("Days remaining this month,", remainingDays)
    allDays = []
    nthDay = 0
    while remainingDays > 0:                        # when days remain, iterate over and create strings of every date
        nthDay = curDay + int(str(diff)[0])
        curDay = nthDay
        allDays.append(str(todaysDate)[0:-2]+ str(curDay))
        remainingDays = remainingDays-1

    print(allDays)
    Message(rightFrame, text = "SELECT DATE-  ").pack(side= TOP)
    dateVar = StringVar(rightFrame)
    dateVar.set(str(todaysDate))
    inputDay = OptionMenu(rightFrame, dateVar, *allDays)
    inputDay.pack(side =TOP)



    def getVal():                                # gfetch input of selected date
        frontEnd.email_text = ""
        for i in Entries:
            frontEnd.email_text += i +" "
        submit.pack_forget()
        createEntry()


    def createmail():                           # convert input to email format 
        frontEnd.email_text = ""
        for i in Entries:
            frontEnd.email_text += i +" \n"
        submit.pack_forget()
        email()

    submit = Button(bottomFrame, text = "submit", command = getVal)
    submit.pack(side = TOP)
    sendButton = Button(bottomFrame, text= "send mail", command = createmail)
    sendButton.pack(side = BOTTOM)
    plannerWindow.mainloop()


def email():                                # compose email and send it to the mail sending function
    email.sent_from = "YOUR ADRESS"
    email.to = "RECIEVERS ADRESS"
    email.subject = "FIRST EMAIL FROM PYTHON!!!!"
    email.body = "\n Sent from %s, \n sent to %s \n \n \n %s \n \n \n \n" % (email.sent_from, email.to, frontEnd.email_text)
    backend.mail(email.sent_from ,email.to, email.body)
frontEnd()