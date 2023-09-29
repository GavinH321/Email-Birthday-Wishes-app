# Extra Hard Starting Project
# importing the required libraries for the project
import pandas as pd
import datetime as dt
import random
import smtplib

# Created variables to use smtp to send emails
my_email = "pythontesting32hensley@gmail.com"
app_password = "ipdvrrzbzjzefodm"
letters = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]
user_email = ""

# Create data to store in a csv file to check to see if it's one of our birthdays
new_data = pd.DataFrame(
    {
        "name": ["Gavin", "Renaee"],
        "email": ["gavinhensley32@gmail.com", "renaeecollier@gmail.com"],
        "year": ["2023", "2000"],
        "month": ["9", "7"],
        "day": ["29", "30"]
    },
    index=range(0, 2)
)
# This line retrieves the exact time
now = dt.datetime.now()

# 1. Update the birthdays.csv
new_data.to_csv(path_or_buf="birthdays.csv", index=False)

# 2. Check if today matches a birthday in the birthdays.csv
is_birthday = False
birthday_name = ""
file = pd.read_csv("birthdays.csv")
for item in file.values:
    if item[3] == now.month and item[4] == now.day:
        birthday_name = item[0]
        user_email = item[1]

if birthday_name != "":
    is_birthday = True

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with
# the person's actual name from birthdays.csv
if is_birthday:
    new_letter = random.choice(letters)
    with open(file=new_letter) as birthday_letter:
        contents = birthday_letter.read()

    with open("Birthday_letter.txt", "w") as updated_letter:
        updated_letter.write(contents.replace("[NAME]", birthday_name))

# 4. Send the letter generated in step 3 to that person's email address.
try:
    with open("Birthday_letter.txt", "r") as letter_to_mail:
        letter = letter_to_mail.read()
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=app_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=user_email,
                            msg=f"Subject:Happy Birthday!\n\n{letter}")
        print("Email has been sent!")
except (FileNotFoundError, NameError):
    print("It's nobody's birthday.")
