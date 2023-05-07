# CareConnect

Inspiration
Industry trends: We are inspired by the growing interest in health and wellness and saw an opportunity to create an app that caters to this market. There are many new trends and innovations in the health industry, from wearable fitness trackers to personalized nutrition plans. With the recent uptick in AI-enhanced software, we saw an opportunity to apply this to personal healthcare.

What it does
Users are able to login or sign up for CareConnect and once logged in they are taken to a page where they have the option to chat with a health bot and ask any questions related to their general health. They also have the option to click the report button where they are able to record their blood pressure, heart rate, and blood glucose level. Users are also able to add a list of their medications so that the application can notify the user when it is time to take their medication by triggering an LED and buzzer on an Arduino. Finally, they are also able to click on the Records button to view graphs of their blood pressure, heart rate, and blood glucose level over time.

How we built it
We used Python to build most of the application. The cohere API was used to create the chatbot, pyFirmata library was used to communicate with the Arduino microcontroller, PySimpleGUI was used for the front end, and Matplotlib was used to create the graphs.

Challenges we ran into
The biggest challenge we had was being able to communicate with the Arduino and using multithreading to ensure that the application is always checking if its time to take their medication. We also had trouble with the MATLAB engine API since we Python and MATLAB versions that were not compatible with each other, this caused us to switch to Matplotlib for the graphs.

Accomplishments that we're proud of
We are proud of the integration of the hardware into the application, especially through the use of concurrency.

What we learned
We learned how to use PySimpleGUI and how to use Python to communicate with a microcontroller. We also learned how to store data in Excel sheets.

What's next for CareConnect
Allow users to send their health records to their doctors and to create a wearable device for the hardware. Also, enhance the front end of the application.

Note: The cohere API key was not included in the Github for security purposes.
