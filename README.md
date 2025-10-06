# FILE-INTEGRITY-CHECKER

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: NIVYA ANTONY

*INTERN ID*: CT04DY2625

*DOMAIN*: CYBER SECURITY AND ETHICAL HACKING

*DURATION*: 4 WEEKS

*MENTOR*: NEELA SANTHOSH

## The task 1 for Cyber Security and Ethical Hacking was to build a tool to monitor changes in files by calculating and comparing hash values. It was instructed to use python libraries like hashlib to ensure file integrity. So the first step was to understand what is hashlib library and hash values. Now it's the time to work out. So I downloaded VS code to run the python script. SHA-256 algorithm in the hashlib module was used to calculate the hash values and these hash values were stored into *file_hashes.json*. A test folder was created and inside that folder 2 text files and the *checker.py* were saved. So when the python script was run the hash values for the files existed in the test folder was calculated and saved to the database. So when we made changes to those file and run the script it was showing the corresponding output in the terminal. After making each changes we should the run the script to see the outputs. I did some modification in this like adding the timestamp by importing 'datetime' module so we get the time of the changes that got done in the file,'colorama' module was imported to add colour to the output so that it will be easier to understand. It will be difficult to run the python script every time if we need to see any changes happened to files. So I thought to make this work as a real time monitoring system. So the 'watchdog' module was imported and every single changes were seen in the terminal without running. Later the output displayed on the terminal were saved into the *integrity_log.txt*.At first these settings worked only when the VS code was opened and outputs were displayed only if we make changes through VS code like opening the folder from the left tab of the VS code. So to rectify this  python script was converted into it's extension named *checker.exe* by installing 'pyinstaller' and added this extension file into the task sheduler in my desktop. After enabling this functionality there was no need to open the VS code. We can simply locate these files from my desktop and can make changes and these changes where written to the *integrity_log* file. Now the task is very simple ,all I need is to check the log file to see any changes. It continously monitors the file creation, deletion, modification and log these events with the timestamp and path details whenever the system boots. Error logging was also included for debugging and records error in seperate file named *error_log.txt*. So this is all about how I completed the task 1. Thank you!

# OUTPUT

<img width="1360" height="725" alt="Image" src="https://github.com/user-attachments/assets/a748f3e0-d582-4f26-99bd-ca99f227486d" />
<img width="1360" height="730" alt="Image" src="https://github.com/user-attachments/assets/9d76f6e8-b07a-4149-b55d-f9a0c058a414" />
<img width="1360" height="734" alt="Image" src="https://github.com/user-attachments/assets/7c87c085-5636-4b8b-86f7-67b2fa235a64" />
