# importing our libraries so that we can use their content.
from tkinter import *
import customtkinter

import subprocess  # for running the keylogger.py file
from sys import platform  # for opening the log file.
import webbrowser  # also for opening the log file.
import re

# Global variables to keep track of whether or not the keylogger is running, and which windows are open.
running = False
openWindows = {}

scriptRunning = None
logFileName = "log.txt"


# Creates the initial window and sets the title and some basic options.
def setup():
    window = customtkinter.CTk()
    window.geometry("1100x580")
    window.title("KeyLogger - Daniel Banks")
    window.resizable(False, False)

    # to handle what happens whenever the user closes the main window.
    def onClose():
        window.destroy()  # destroy everything to do with the application.

        if running:  # if they were running the keylogger script, stop it.
            subprocess.Popen.terminate(scriptRunning)

    window.protocol("WM_DELETE_WINDOW", onClose)

    customtkinter.set_appearance_mode("dark")
    return window


# Will start or stop the keylogger.
def click_activate_button(button):
    # the global variable declaration so we can modify the value of it.
    global running
    global scriptRunning

    if not running:  # then we should start running the logger as it is currently OFF
        # Running the keylogger script using the subproccess module.
        scriptRunning = subprocess.Popen(["python3", "keylogger.py"])

        running = True  # change the value of the global variable
        # change the styling of the button
        button.configure(text="STOP KEYLOGGER",
                         hover_color="darkred", fg_color="red")
    else:  # we should disable the keylogger
        # stop the keylogger script from running using subprocess
        subprocess.Popen.terminate(scriptRunning)
        # refresh the items in the list using the method defined below.
        refreshItems()

        running = False
        button.configure(text="START KEYLOGGER",
                         hover_color="darkgreen", fg_color="green")

# Will create and design our initial activate button.


def activate_button():
    # set the parent of the element to the sidebar, and assign some basic options such as width, height, initial text, foreground color, and the hover color.
    sidebar_activate_button = customtkinter.CTkButton(
        sidebar_frame, width=75, height=40, text="START KEYLOGGER", fg_color="green", hover_color="darkgreen")

    # assigning a callback for whenever the button is pressed, in this case we will call the "click_activate_button" function when this button is pressed.
    sidebar_activate_button.configure(
        command=lambda arg=sidebar_activate_button: click_activate_button(arg))
    return sidebar_activate_button


# Opening a new window to reveal the logs of that given day.
# frameName is our date (also the key in the dict) and logs is our actual log string.
def openLogPopout(event, frameName, logs):

    # so the same popup cannot open twice.
    if openWindows.keys().__contains__(frameName):
        return

    # creating the new window and assigning some basic options (title, width, height) and locking the minimum size of the window.
    newWindow = Toplevel(root)
    newWindow.title(frameName)
    newWindow.geometry("900x600")
    newWindow.minsize(width=900, height=600)

    # creating the header which will display the date of the log provided.
    dateHeader = customtkinter.CTkLabel(
        newWindow, text=frameName, font=customtkinter.CTkFont("Arial", weight="bold", size=30))

    # row 0 so that it will be at the top of our window on the first row. And some padding just to improve looks.
    dateHeader.grid(row=0, column=0, padx=20, pady=30)

    # This will ensure that every 100 characters there is a new line so that the text is not going off of the window.
    def formatRawLog(logString):
        # initial variables which will be used through the iterations.
        count = 0
        formatted = ""

        if logString == "":
            return "No Keys Captured."

        # loop through every letter of the log string
        for letter in logString:
            # if the count is less than 100 then we can just carry on as normal, and append the letter to our new string, and increment the count.
            if count < 100:
                formatted += letter
                count += 1
                continue
            else:  # otherwise, we want to add a new line as there is now 100 characters on that line, and then set the count back to 0 otherwise we would have a new line before every letter going on with the loop.
                formatted += "\n{0}".format(letter)
                count = 0

        return formatted

    # Displaying the raw output text using the function above. Also assinging some styling options such as anchor, compound and justify.
    rawOutputHeader = customtkinter.CTkLabel(newWindow, text="Raw Output", font=customtkinter.CTkFont(
        "Arial", weight="bold", size=21), anchor="w", width=700, justify="left", compound="left")
    rawOutput = customtkinter.CTkLabel(newWindow, text=formatRawLog(
        logs), anchor="w", compound="left", width=700, justify="left")

    # Displaying both of these elements onto the screen using the grid method. Row 1 and 2 so that they are in the order they are meant to be in (the header being above the actual log)
    rawOutputHeader.grid(row=1, column=0, padx=50)
    rawOutput.grid(row=2, column=0, padx=50, pady=2)

    # Will replace all the Special text characters and irrelevant spaces and also ensure that every 100 characters there is a new line so that the text is not going off of the window.

    def formatLog(logString):
        if logString == "":
            return "No Keys Captured."

        # replace all of the Key.spaces with actual spaes and remove all other spaces.
        formatted = logString.replace(" ", "").replace("Key.space", " ")

        # Regex to remove all other instances of special keys.
        regex = r"Key.\w*"
        subst = ""
        result = re.sub(regex, subst, formatted, 0)

        count = 0
        withLimits = ""
        for letter in result:
            if count < 100:
                withLimits += letter
                count += 1
                continue
            else:
                withLimits += "\n{0}".format(letter)
                count = 0

        return withLimits

    # Displaying the formatted output header and the actual output itself using the function above.
    formattedOutputHeader = customtkinter.CTkLabel(newWindow, text="Formatted Output", font=customtkinter.CTkFont(
        "Arial", weight="bold", size=21), anchor="w", width=700, justify="left", compound="left")
    formattedOutput = customtkinter.CTkLabel(newWindow, text=formatLog(
        logs), anchor="w", compound="left", width=700, justify="left")

    # Putting the elements into the window using the grid method. Using rows 3 and 4 so that they go underneath our raw outputs.
    formattedOutputHeader.grid(row=3, column=0, padx=50)
    formattedOutput.grid(row=4, column=0, padx=50, pady=2)

    # a method which will be called whenever the window is closed, the window will be removed from our "openWindows" dict which keeps track of all the windows. The destroy method is also called to cleanup any loose pieces.
    def onClose():
        openWindows.__delitem__(frameName)
        newWindow.destroy()

    # Adding the callback to the delete window protocol - (the function will be called whenever the user closes this window)
    newWindow.protocol("WM_DELETE_WINDOW", onClose)

    # Adding our window to the openWindows dict.
    openWindows[frameName] = newWindow


# calling our setup function creating our initial parent window.
root = setup()


# ---------------------------------
# Creating the sidebar

# creating the actual frame which all our sidebar elements will nest inside of.
sidebar_frame = customtkinter.CTkFrame(
    root, width=200, height=580, fg_color="#222")
sidebar_frame.grid(row=0, column=0)

# Create the title and place it in the center of the frame.
sidebar_title = customtkinter.CTkLabel(sidebar_frame, text="KeyLogger", fg_color="transparent",
                                       font=customtkinter.CTkFont("Arial", weight="bold", size=21), height=200)
sidebar_title.place(relx=0.5, rely=.05, anchor=CENTER)

# Clear logs button, when clicked will clear the log.txt file.
sidebar_clear_logs_button = customtkinter.CTkButton(
    sidebar_frame, text="Clear All Logs", fg_color="red", width=75, height=40, hover_color="darkred")
sidebar_clear_logs_button.place(relx=0.5, rely=.6, anchor=CENTER)


def clearLogFile():
    # opening the file in write mode will automatically wipe the file.
    open(logFileName, "w").close()

    # Loop through all the log objects and destroy them
    try:
        for child in log_frame.children.values():
            child.destroy()
    except:
        pass


# Assigning the clearLogFile method to the command value of the button. Meaning it is called whenever button is clicked.
sidebar_clear_logs_button.configure(command=clearLogFile)

# Creating the open logs button, which will open the log file in their default text editor.
sidebar_logs_button = customtkinter.CTkButton(
    sidebar_frame, text="Open Logs File", fg_color="blue", width=75, height=40, hover_color="darkblue")
sidebar_logs_button.place(relx=0.5, rely=.69, anchor=CENTER)


def openLogsFile():
    # if the user is on macOS, we will open the file with TextEdit
    if platform.startswith("darwin"):
        subprocess.call(['open', '-a', 'TextEdit', logFileName])
    # Otherwise, we will open with the default system text editor.
    elif platform.startswith("win"):
        webbrowser.open(logFileName)


# Assigning the openLogsFile method to the command value of the button. Meaning it is called whenever button is clicked.
sidebar_logs_button.configure(command=openLogsFile)


# Create the activate button and also place it in the center but towards the bottom of the frame.
sidebar_activate_button = activate_button()
sidebar_activate_button.place(relx=0.5, rely=.85, anchor=CENTER)

# ----------------------------------
# Creating the log showings

# create the log frame which all the elements below will nest inside of.
big_log_frame = customtkinter.CTkFrame(
    root, width=900, height=580, fg_color="transparent")


# notice column 1 now, so that its displayed separately to the sidebar.
big_log_frame.grid(row=0, column=1)


# creating the big LOGS title so the user knows what this section displays.
log_title = customtkinter.CTkLabel(big_log_frame, text="LOGS", fg_color="transparent",
                                   bg_color="transparent", font=customtkinter.CTkFont("Arial", weight="bold", size=40), height=80)
log_title.grid(row=0, column=1)

# a scrollable frame which will nest all of the logs from the "log.txt" file. Users will be able to scroll through all the logs within this element with the scrollbar provided.
log_frame = customtkinter.CTkScrollableFrame(
    big_log_frame, width=800, height=400, fg_color="#333")
log_frame.grid(row=1, column=1, pady=15, padx=40)


# open the actual log file in read mode.
def updateItems():
    file = open(logFileName, "r")

    # create a dict to store all the logs.
    logDict = {}

    # to iterate through all the lines within the file.
    finished = False
    while not finished:
        # the current line being read
        line = file.readline()
        if line == "":  # if its nothing, then we're at the end of the file so can stop the loop.
            finished = True
            break
        elif line == "\n":  # if its a new line we can just carry on.
            continue
        else:  # if its not a newline it means we found text, and the first text is always our date. So now in theory the "line" variable represents our date.
            # we read the next line which will be the actual logs.
            content = file.readline()
            # we then store the logs inside the dict using the date as the key.
            logDict[line.replace("\n", "")] = content

    # close the file to save resources and avoid opening it twice.
    file.close()

    # looping through all the logs to display them in the scrollable frame.
    counter = 0
    for date, logs in logDict.items():

        # Creating an initial frame which will be going inside of the scrollable. We also make it so if a user hovers over this the cursor will change to a differnt one.
        entryFrame = customtkinter.CTkFrame(
            log_frame, width=500, height=100, fg_color="#222", cursor="center_ptr")

        # Using bind to recognise whenever a user has clicked on the frame. When they have, our callback will be executed which is the openLogPopout method defined above.
        entryFrame.bind("<Button-1>", lambda event, frameName=date,
                        log=logs: openLogPopout(event, frameName, log))

        # Using the counter value as our row so that all the elements dont just place on top of each other.
        entryFrame.grid(column=0, row=counter, padx=150, pady=5)

        # Adding the date of the log to the frame so that the user knows what each frame represents.
        entryTitle = customtkinter.CTkLabel(
            entryFrame, text=date, text_color="#fff", font=customtkinter.CTkFont("Arial", size=22))

        # Placing the text in the center of the frame.
        entryTitle.place(anchor="center", relx=0.5, rely=0.5)

        # incrementing the counter by 1.
        counter += 1

# Will be called whenever the keylogger is disabled. Therefore, updating the scrollable list with the newly created logs.


def refreshItems():
    # destroy all the children currently in the list.
    log_frame.children.clear()
    updateItems()  # re-create them all again.


# start the application loop and update the items in the logs list.
updateItems()
root.mainloop()
