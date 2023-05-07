import PySimpleGUI as sg
import cohere
import simplethreads
from cohere.responses.classify import Example
import csv
import pyfirmata as pyf
import board
#simplethreads.ThreadPool import ThreadPool
import asyncio
import time
import threading
import datetime
import matplotlib.pyplot as plt
import serial
#import matlab.engine
#import pulseio
# see all the themes
# sg.theme_previewer()
LEDPin = 4
buzzerPin = 'd:3:p'
projectName = 'CareConnect'

co = cohere.Client('BAyOeaK39IacOJbdXERo5qSMOTu56uWCvEzei8zt')
#eng = matlab.engine.start_matlab()
board = pyf.Arduino('COM4')
#ser = serial.Serial('COM4', 9600)
buzzer = board.get_pin(buzzerPin)

user = ''


times = []
examples = [Example("i have a headache, what should i do?", "general help"),
            Example("i am bleeding", "general help"),
            Example("i have a cough", "general help"),
            Example("i have a sore throat", "general help"),
            Example("is 120/80 blood pressure normal?", "general help"),
            Example("What is consider high blood sugar?", "general help"),
            Example("my sister fell and rolled her ankle and it is swollen what should she do?", "general help"),
            Example("what can i do to prevent heart disease?", "general help"),
            Example("what type of medication can i use for a cold", "general help"),
            Example("why can't i sleep?", "general help"),
            Example("should i take a multivitamin?", "general help"),
            Example("why do i need a yearly checkup?", "general help"),
            Example("should i see my provider for a cold?", "general help"),
            Example("My tooth hurts what should i do?", "general help"),
            Example("how long am i contagious with the flu?", "general help"),
            Example("is advil medicine good for pain?", "general help"),
            Example("Is it true that 48 hours after starting antibiotics I can't infect someone else?", "general help"),
            Example("Is bird flu still a danger?", "general help"),
            Example("how often should i get my teeth professionally clean?", "general help"),
            Example("will staring at a computer all day long make me go blind?", "general help"),

            Example("i want to add a medication to my medication list", "medication"),
            Example("i want to add a medication", "medication"),
            Example("my doctor prescribed me a new medication", "medication"),
            Example("what medications am i taking?", "medication"),
            Example("medication list", "medication"),
            Example("when do i need to take my medicine?", "medication"),
            Example("my provider has prescribed me a insulin injection", "medication"),
            Example("i have a new cholesterol medication", "medication"),

            Example("can i see me health records?", "records"),
            Example("health records", "records"),
            Example("what are my health trends?", "records"),
            Example("what was my blood pressure yesterday?", "records"),
            Example("i want to send my doctor my health data", "records"),

            Example("id like to report my blood pressure", "report"),
            Example("my heartrate is 90bpm", "report"),
            Example("report my health", "report"),

            ]


def callAI(input):
    response = co.classify(inputs = [input], examples = examples)
    return response

def generateAIText(input):
    response = co.generate(
        model='command-xlarge-nightly',
        prompt = input,
        max_tokens = 300,
        temperature = 0.9,
        k = 0,
        stop_sequences = [],
        return_likelihoods = 'NONE')
    return response.generations[0].text

def signUp(username, pw):
    with open('Database.csv',  encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        # Iterate over the rows and print a specific element
        for row in reader:
            if(row[0] == username):
                return False
    with open('Database.csv', 'a',  newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow([username, pw])

    with open(f'{username}MEDS.csv', 'w'):
            pass
    with open(f'{username}DATA.csv', 'w'):
            pass
    return True

def logIn(username, pw):
    with open('Database.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if(row[0] == username and row[1] == pw):
                return True
    return False

def writeMedication(username, name, dosage, freq, time):
    with open(f'{username}MEDS.csv', 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow([name, dosage, freq] + time)

def reportHealth(username, hr,  bps, bpd, glucose):
    now = datetime.datetime.now()
    nowStr = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(f'{username}DATA.csv', 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow([nowStr, hr, bps, bpd, glucose])
    print("Success! Data reported.")

def updateMedSummary(username):
    #print('Updating summary')
    out = ''
    with open(f'{username}MEDS.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        times.clear()

        for row in reader:
            count +=1
            out += (f'Medication {count}: {row[0]}\nDosage: {row[1]}\nDaily Frequency: {row[2]}\nTimes: ')
            count2 = 0
            for i in row:
                if (count2 <= 2):
                    count2 += 1
                else:
                    #print(row[count2])
                    out += f'{row[count2].strip("),"),}'
                    times.append(row[count2])
                    count2 += 1

            out += '\n\n'
    return out

def graphs(username):
    hr = []
    bps = []
    bpd = []
    glu = []
    with open(f'{username}DATA.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            hr.append(row[1])
            bps.append(row[2])
            bpd.append(row[3])
            glu.append(row[4])
    plt.figure()
    plt.plot(hr)
    plt.title("Heart Rate Records")
    plt.ylabel("HeartRate (BPM)")
    plt.figure()
    plt.plot(bpd, label="Systolic Pressure")
    plt.plot(bps, label="Diastolic Pressure")
    plt.title("Blood Pressure Records")
    plt.ylabel("Blood Pressure (mmHg)")
    plt.figure()
    plt.plot(glu)
    plt.title("Blood Glucose Levls")
    plt.ylabel("Blood Glucose Level (mmol/L)")
    plt.show()


def checkMedication(username):
    while True:
        #print('Checking Medication')
        now = datetime.datetime.now()
        nowStr = now.strftime("%H:%M")
        if nowStr in times:

            arduinoStuff()
        time.sleep(10)





# def heartRateSensor():
#     print("in func")
#     it = pyf.util.Iterator(board)
#     it.start()
#     analogInput = board.get_pin('a:0:i')
#
#     while True:
#         analogValue =ser.readline()
#         heartRate = analogValue * 100/1023
#         print(heartRate)
#         # analogValue = analogInput.read()
#         # if analogValue is not None:
#         #     print(f'A0 Values: {analogValue}')
#         #     heartRate = analogValue * 100
#         #     print(heartRate)
#         # else:
#         #     print("sleep")
#         #     time.sleep(3)


sg.theme('LightBlue')  # Add a touch of color
sg.set_options(font='Calibri 20')

# All the stuff inside your window.
# layout contains all the visible elements on the screen
# each list is its own row

button_size = (10, 3)

layoutOpen0 = [
        [sg.Text(f"{projectName}", font = 'Helvetica 30', pad = (50,0))],
        [sg.Image('logo.png', size=(300,300))],
        [sg.Text("Your AI Health Companion")],
        [sg.Button("Login", key = '-L1LOGIN-'), sg.Button("Sign Up", key = '-L1SIGNUP-')]
]

layoutOpen = [
    [sg.VPush()],
    [sg.Column(layoutOpen0, element_justification='center')],
    [sg.VPush()]

]

layoutLogin = [
[sg.Push(), sg.Text(f'{projectName}', key='-TEXT1-'),sg.Image('logoS.png', size=(30,30)),sg.Push()],
    [sg.VPush()],
    [sg.Push(), sg.Text("Username: "), sg.Input(key='-LUSERFIELD-'), sg.Push()],
    [sg.Push(), sg.Text("Password: "), sg.Input(key='-LPASSFIELD-'), sg.Push()],
    [sg.Push(), sg.Button("Login", key='-LOGINBTN-'),sg.Button("Return", key='-LOGINRBTN-'), sg.Push()],
    [sg.Push(), sg.Text("temp", visible=False, key='-ERRORTXT1-'), sg.Push()],
    [sg.VPush()]
]

layoutSignup = [
[sg.Push(), sg.Text(f'{projectName}', key='-TEXT1-'),sg.Image('logoS.png', size=(30,30)),sg.Push()],
    [sg.VPush()],
    [sg.Push(),  sg.Text("Username: "),sg.Input(key = '-SUSERFIELD-'), sg.Push()],
    [sg.Push(),  sg.Text("Password: "),sg.Input(key = '-SPASSFIELD-'), sg.Push()],
    [sg.Push(), sg.Button("Sign Up", key = '-SIGNUPBTN-'), sg.Button("Return", key = '-SIGNUPRBTN-'), sg.Push() ],
    [sg.Push(), sg.Text("temp", visible = False, key = '-ERRORTXT2-'), sg.Push()],
    [sg.VPush()]
]

layoutMain = [[sg.Push(), sg.Text(f'{projectName}', key='-TEXT1-'),sg.Image('logoS.png', size=(30,30)),sg.Push()],
              [sg.VPush()],
              [sg.Output(size = (300, 30),font=('Helvetica 10'))],
              [sg.VPush()],
              [sg.Button('Enter', key='-ENTERBTN-', size=(7,2)), sg.Multiline(size=(45, 2), key='-INPUT-')],
              [sg.Push(), sg.Button('Report', key='-BTN1-', size=button_size, pad = (2,0)), sg.Push(),
               sg.Button('Records', key='-BTN2-', size=button_size, pad = (2,0)), sg.Push(),
               sg.Button('Meds', key='-BTN3-', size=button_size, pad = (2,0)), sg.Push()]]

layoutMeds = [
[sg.Push(), sg.Text(f'{projectName}', key='-TEXT1-'),sg.Image('logoS.png', size=(30,30)),sg.Push()],
            [sg.Push(), sg.Text("Medication Summary"), sg.Push()],
            [sg.Multiline("", size =(400,10), key = '-MEDSUM-')],
            [sg.Push(), sg.Button("New",  key = '-NEWMEDS-'), sg.Button("Return", key = '-MEDSRETURN-')],

]

layoutReport = [
[sg.Push(), sg.Text(f'{projectName}', key='-TEXT1-'),sg.Image('logoS.png', size=(30,30)),sg.Push()],
            [sg.Push(), sg.Text("Report Data", font = ('Helvetica 15')), sg.Push()],
            [sg.Push(), sg.Text("Heart Rate (bpm): "), sg.Input(key = '-HRFIELD-'), sg.Text("bpm"), sg.Push()],
            [sg.Push(), sg.Text("Blood Pressure (sys) (mmHg): "), sg.Input(key = '-BPSFIELD-'), sg.Text("mmHg"), sg.Push()],
            [sg.Push(), sg.Text("Blood Pressure (dia) (mmHg): "), sg.Input(key = '-BPDFIELD-'), sg.Text("mmHg"), sg.Push()],
            [sg.Push(), sg.Text("Glucose (mmol/L): "), sg.Input(key = '-GLUFIELD-'), sg.Text("mmol/L"), sg.Push()],
            [sg.Push(), sg.Button("Submit", key = '-SUBMITREPORT-'), sg.Button('Return', key = '-RETURNREPORT-'), sg.Push()],
]

layoutData = []

layoutNewMeds = [
    [sg.VPush()],
[sg.Push(), sg.Text(f'{projectName}', key='-TEXT1-'),sg.Image('logoS.png', size=(30,30)),sg.Push()],
            [sg.Push(), sg.Text("New Medication", font = ('Helvetica 15')), sg.Push()],
            [sg.Push(), sg.Text("Name: "), sg.Input(key = '-MEDNAMEFIELD-'), sg.Push()],
            [sg.Push(), sg.Text("Dosage(mg): "), sg.Input(key = '-MEDDOSEFIELD-'), sg.Push()],
            [sg.Push(), sg.Text("Daily Frequency: "), sg.Input(key = '-MEDFREQFIELD-'), sg.Push()],
            [sg.Push(), sg.Text("Times: "), sg.Input(key = '-MEDTIMEFIELD-'), sg.Push()],
            [sg.Push(), sg.Button("Submit", key = '-SUBMITNEWMED-'), sg.Button('Return', key = '-RETURNNEWMED-'), sg.Push()],
            [sg.VPush()]
]

layout = [[sg.Column(layoutOpen, key='-COL1-'),
           sg.Column(layoutLogin, visible=False, key='-COL2-'),
           sg.Column(layoutSignup, visible=False, key='-COL3-'),
           sg.Column(layoutMain, visible=False, key='-COL4-'),
           sg.Column(layoutMeds, visible=False, key='-COL5-'),
           sg.Column(layoutReport, visible=False, key='-COL6-'),
           sg.Column(layoutData, visible=False, key='-COL7-'),
           sg.Column(layoutNewMeds, visible=False, key='-COL8-'),
           ]]

chat = []

# Create the Window
window = sg.Window(f'{projectName}', layout, size=(648, 1152), location=(0,0), finalize = True, element_justification = 'center')
print("Carey: \nWelcome to CareConnect, I'm Carey, your AI health counsellor. Type your medical prompt in the box below...\n"
      "Here are some examples of things you can say:\n"
      "'My head hurts, what are some things I can do to help it?'\n"
      "'Will staring at a computer all day long make me go blind?'\n"
      "'I want to add a medication to my medication list'\n"
      )



# Event Loop to process "events" and get the "values" of the inputs

async def main():

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break

        ## event code for main screen
        if event == '-L1LOGIN-':
            window['-COL1-'].update(visible=False)
            window['-COL2-'].update(visible=True)

        if event == '-L1SIGNUP-':
            window['-COL1-'].update(visible=False)
            window['-COL3-'].update(visible=True)


        ## event code for login screen
        if event == '-LOGINBTN-':
            val = logIn(values['-LUSERFIELD-'], values['-LPASSFIELD-'])
            if val:
                window['-COL2-'].update(visible=False)
                window['-COL4-'].update(visible=True)

                user = values['-LUSERFIELD-']
                #print(user)
                updateMedSummary(user)
                background_thread = threading.Thread(target=checkMedication, args=(user,))
                background_thread.daemon = True
                background_thread.start()

            else:
                window['-ERRORTXT1-'].update("Invalid Login.")
                window['-ERRORTXT1-'].update(visible = True)
        if event == '-LOGINRBTN-':
            window['-COL2-'].update(visible=False)
            window['-COL1-'].update(visible=True)

        ## event code for signup screen

        if event == '-SIGNUPBTN-':
            val = signUp(values['-SUSERFIELD-'], values['-SPASSFIELD-'])
            if val:
                window['-COL3-'].update(visible=False)
                window['-COL4-'].update(visible=True)

                user = str((values['-SUSERFIELD-']))
                updateMedSummary(user)
                background_thread = threading.Thread(target=checkMedication, args=(user,))
                background_thread.daemon = True
                background_thread.start()

            else:
                window['-ERRORTXT2-'].update("Username already taken.", visible = True)

        if event == '-SIGNUPRBTN-':
            window['-COL3-'].update(visible=False)
            window['-COL1-'].update(visible=True)

        ## main screen events

        if event == '-BTN1-':
            window['-COL4-'].update(visible=False)
            window['-COL6-'].update(visible=True)

        if event == '-BTN2-':
            graphs(user)

        if event == '-BTN3-':
            window['-COL4-'].update(visible=False)
            window['-COL5-'].update(visible=True)
            window['-MEDSUM-'].update(updateMedSummary(user))
            #print(times)

        if event in ['-ENTERBTN-']:

            text = values['-INPUT-']

            chat.append([0, text])
            print(f'{user}:')
            print(f'{text}')
            response = callAI(values['-INPUT-'])
            window['-INPUT-'].update('')

            label = response.classifications[0].prediction
            ##print(label)

            if  label == 'general help':
                resp = generateAIText(text)
                print(f'Carey: {resp}')
                print('')
            if label == 'medication':
                ## swich to medication page
                window['-COL4-'].update(visible=False)
                window['-COL5-'].update(visible=True)
                window['-MEDSUM-'].update(updateMedSummary(user))

            if label == 'record':
                ## switch to records tab
                pass
            if label == 'report':
                window['-COL4-'].update(visible=False)
                window['-COL6-'].update(visible=True)


        ## events for report page
        if event == '-SUBMITREPORT-':
            reportHealth(user, values["-HRFIELD-"], values["-BPSFIELD-"], values["-BPDFIELD-"], values["-GLUFIELD-"])
            window['-COL6-'].update(visible=False)
            window['-COL4-'].update(visible=True)
            window['-HRFIELD-'].update('')
            window['-BPSFIELD-'].update('')
            window['-BPDFIELD-'].update('')
            window['-GLUFIELD-'].update('')
        if event == '-RETURNREPORT-':
            window['-COL6-'].update(visible=False)
            window['-COL4-'].update(visible=True)


        ## events for medication page
        if event == '-MEDSRETURN-':
            window['-COL5-'].update(visible=False)
            window['-COL4-'].update(visible=True)

        if event == '-NEWMEDS-':
            window['-COL5-'].update(visible=False)
            window['-COL8-'].update(visible=True)


        ## events for new medication
        if event == '-SUBMITNEWMED-':
            writeMedication(user, values["-MEDNAMEFIELD-"],
                            values["-MEDDOSEFIELD-"],
                            values["-MEDFREQFIELD-"],
                            values["-MEDTIMEFIELD-"].split(","))
            window['-COL8-'].update(visible=False)
            window['-COL5-'].update(visible=True)
            window['-MEDSUM-'].update(updateMedSummary(user))
            window['-MEDNAMEFIELD-'].update('')
            window['-MEDDOSEFIELD-'].update('')
            window['-MEDFREQFIELD-'].update('')
            window['-MEDTIMEFIELD-'].update('')


        if event == '-RETURNNEWMED-':
            window['-COL8-'].update(visible=False)
            window['-COL5-'].update(visible=True)



def arduinoStuff():
    print("Arduino Activating")
    board.digital[LEDPin].write(1)

    buzzer.write(16)
    time.sleep(3)
    board.digital[LEDPin].write(0)
    buzzer.write(0)



#print(heartRateSensor())

asyncio.run(main())
#asyncio.run(print(heartRateSensor()))
#pool.shutdown(block = False)
board.exit()
window.close()
