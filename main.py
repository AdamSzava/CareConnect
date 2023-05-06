import PySimpleGUI as sg
import cohere
from cohere.responses.classify import Example
import csv
import os
import pandas as pd
# see all the themes
# sg.theme_previewer()

projectName = 'CareConnect'
co = cohere.Client('BAyOeaK39IacOJbdXERo5qSMOTu56uWCvEzei8zt')


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
            Example("how often should i get my teeth professionaly clean?", "general help"),
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
            ]
def callAI(input):
    response = co.classify(inputs = input, examples = examples)
    return response

def gnerateAIText(input):
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
    for index, row in df.iterrows():
        if(row['Username'] == username):
            print("username exists already, pick another")
            break
        if index == len(df) - 1:
            with open('Database.csv', 'a') as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow(['Username'])
                filewriter.writerow([Username])

def logIn(username, pw):
    return

def writeData(type, value):
    return

sg.theme('LightBlue')  # Add a touch of color
sg.set_options(font='Calibri 20')

# All the stuff inside your window.
# layout contains all the visible elements on the screen
# each list is its own row

button_size = (10, 3)

layoutMain = [[sg.Push(), sg.Text(f'{projectName}', key='-TEXT1-'), sg.Push()],
              [sg.VPush()],
              [sg.Output(size=(110, 50), font=('Helvetica 10'))],
              [sg.VPush()],
              [sg.Button('Enter', key='-ENTERBTN-', size=button_size), sg.Multiline(size=(45, 2), key='-INPUT-')],
              [sg.Push(), sg.Button('Report Symptoms', key='-BTN1-', size=button_size),
               sg.Button('See Records', key='-BTN2-', size=button_size),
               sg.Button('Options', key='-BTN3-', size=button_size), sg.Push()]]

layoutOptions = [
    [sg.Push(), sg.Button("Button1"), sg.Push()],
    [sg.Push(), sg.Button("Button2"), sg.Push()],
    [sg.Push(), sg.Button("Button3"), sg.Push()],
    [sg.VPush()],
    [sg.Push(), sg.Button("Return"), sg.Push()]
]

chat = []

# Create the Window
window = sg.Window(f'{projectName}', layoutMain, size=(400, 400))
# Event Loop to process "events" and get the "values" of the inputs
while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel

        break

    if event in ['-ENTERBTN-']:
        chat.append([0, values['-INPUT-']])
        print(f'User: {values["-INPUT-"]}')
        response = callAI(values['-INPUT-'])
        print(f'Bot: {response}')
        chat.append([1, response])
        window['-INPUT-'].update('')

window.close()
