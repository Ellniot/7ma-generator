# for picking exercises
import random
# for loading emails
import csv
# to call the shell email sender script and check for the email list file
import os
# to get the date
import datetime

# minimum number of minutes
MIN_MINUTES = 7

# outputted email subject & body filenames
EMAIL_SUBJECT_FILENAME = "email_subject.txt"
EMAIL_BODY_FILENAME = "email_body.txt"

# EXERCISES TO PICK FROM
# [choice weight, 'name', [times it can be done for]]
# weights are 0-100, 0 will never be picked, 100 will always - NOT CURRENTLY USED
EXERCISES = [
    [50, 'plank', [1, 1.5, 2, 2.5, 3]],
    [50, 'side planks (switch @ half)', [1, 1.5, 2]],
    [50, 'side planks w/ dips (switch @ half)', [1, 1.5, 2]],
    [50, 'reverse plank', [1, 1.5, 2, 2.5]],
    [50, 'star plank', [1, 1.5, 2]],
    [50, 'thread the needle planks', [1, 1.5, 2]],
    [50, 'elbow slap planks', [30, 45, 1]],
    [50, 'crunches', [30, 45, 1, 1.5]],
    [50, 'reverse crunches', [30, 45, 1, 1.5]],
    [50, 'side crunches (switch @ half)', [1, 1.5, 2]],
    [50, 'cross crunches', [30, 45, 1, 1.5]],
    [50, 'sit-ups', [30, 45, 1, 1.5]],
    [50, 'peguins', [30, 45, 1, 1.5]],
    [50, 'bicycles', [30, 45, 1, 1.5]],
    [50, 'russian twists', [30, 45, 1, 1.5]],
    [50, 'mountain climbers', [30, 45, 1, 1.5]],
    [50, 'hallow hold', [30, 45, 1, 1.5]],
    [50, 'superman', [30, 45, 1, 1.5]],
    [50, 'pacer pushups', [30, 45, 1, 1.5]],
    [50, 'flutterkicks', [30, 45, 1, 1.5]],
    [50, 'leg lifts', [30, 45, 1, 1.5]],
    [50, 'side leg lifts (switch @ half)', [1, 1.5, 2]],
    [50, 'in-n-outs', [30, 45, 1, 1.5]],
    [50, 'iron cross', [30, 45, 1, 1.5]],
    [50, 'straight arm sit-ups', [30, 45, 1, 1.5]],
    [50, 'pilates 100', [30, 45, 1, 1.5]],
]

def pick_exercises():
    total_time = 0
    exercise_list = []
    chosen_indexes = []

    while total_time < MIN_MINUTES:
        # pick an index of an exercise NOT based on weight
        chosen_index = random.randrange(len(EXERCISES))
        # if the chosen index has already been picked, choose again
        while chosen_index in chosen_indexes:
            chosen_index = random.randrange(len(EXERCISES))
        exercise_name = EXERCISES[chosen_index][1]

        # add the chosen exercise index to the list
        chosen_indexes.append(chosen_index)

        # choose the length of time for this exercise from the time list
        exercise_len_index = random.randrange(len(EXERCISES[chosen_index][2]))
        exercise_len = EXERCISES[chosen_index][2][exercise_len_index]

        # add the suffix to the string
        if exercise_len < 10:
            suffix = " Minutes"
        else:
            suffix = " Seconds"

        # add the exercise name & time to the list
        temp_array = []
        temp_array.append(exercise_name)
        temp_array.append((str(exercise_len) + suffix))
        exercise_list.append(temp_array)

        # add the exercise len to the total time
        if exercise_len > 10:
            if exercise_len == 30:
                total_time = total_time + .5
            elif exercise_len == 45:
                total_time = total_time + .75
        else:
            total_time = total_time + exercise_len

    return [exercise_list, total_time]
        

# fills the passed string with spaces until it reaches the given length
def fill_blank_space(string, length):
    while len(string) < length:
        string = string + " "
    return string

# formats the generated list to a more redable list
def format_email_list(exercise_list, total_mins):
    # find the exercise with the longest string
    longest_str_len = 0
    for exercise in exercise_list:
        if len(exercise[0]) > longest_str_len:
            longest_str_len = len(exercise[0])
    
    # add all exercises to the formatted list
    formatted_list = fill_blank_space("Exercises", longest_str_len) + " | Time       \n"

    # create the spacer
    spacer_str = ""
    while len(spacer_str) < (len(formatted_list) -1 ): # -1 for the \n char
        spacer_str = spacer_str + "-"
    formatted_list = formatted_list + spacer_str + "\n"

    # add the exercises
    for ex in exercise_list:
        formatted_list = formatted_list + fill_blank_space(ex[0], longest_str_len) + " | " + ex[1] + " \n"

    # add the total
    formatted_list = formatted_list + spacer_str + "\n"
    formatted_list = formatted_list + fill_blank_space("Total Minutes", longest_str_len) + " | " + str(total_mins) + " Minutes"

    return formatted_list

# check if there is an "email_list.csv", otherwise create one
def load_eamils():
    # TODO check current dir for "email_list.csv"

    # TODO create a blank email_list.csv

    # otherwise get the list of emails
    with open('email_list.csv') as emailCSV:
        csvReader = csv.reader(emailCSV)
        # should only be one row
        emailList = []
        for row in csvReader:
            emailList.append(row[0])
        return emailList

# save the email body to a txt file, return the date as the subject
def save_email_body(formatted_workout):
    # get todays date & format it
    now = datetime.datetime.now()
    # TODO - fix days like "02nd" -> 2nd
    # get the ending of the date # ('st', 'nd', 'rd' or 'th')
    if now.strftime('%d')[-1] == "1":
        date_end = "st"
    elif now.strftime('%d')[-1] == "2":
        date_end = "nd"
    elif now.strftime('%d')[-1] == "3":
        date_end = "rd"
    else:
        date_end = "th"
    date_str = now.strftime('7MA: %A, %B %d') + date_end

    # save the email body to a file
    email_body_file=open(EMAIL_BODY_FILENAME,'w')
    email_body_file.write(formatted_workout)
    email_body_file.close()

    return date_str


def send_emails(email_list, subject):
    for email in email_list:
        # call the sender script
        os.system('cat ./' + EMAIL_BODY_FILENAME + ' | mutt -s "' + subject + '" ' + email)


def main():
    
    # generate the exercises
    random.seed(a=None, version=2)
    exercise_list_time = pick_exercises()
    
    # format the exercises to look pretty
    exercise_list = exercise_list_time[0]
    total_time = exercise_list_time[1]
    formatted_list = format_email_list(exercise_list, total_time)
    subj = save_email_body(formatted_list)


    # check if there is an email list file in the folder
    path = os.getcwd() + "\\email_list.csv"
    if os.path.exists(path):
        
        # import the emails
        email_list = load_eamils()

        send_emails(email_list, subj)

    else:
        print(formatted_list)
        
    return 0

main()
