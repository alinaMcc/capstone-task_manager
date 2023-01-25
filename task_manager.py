#=====Importing Libraries===========
from datetime import date
from datetime import datetime
import os

#====Define Functions====

def user_login(name, password):

    # Check if username is in the dictionary, if name and password match, return access as True
    while True:
        if name in user_dict:
            if password == user_dict[name]:  # Match password to correct user password
                access_status = True
                break
            else:
                password = input("Please enter a valid password: ")
        else:
            name = input("Please enter a valid username: ")

    return access_status

def reg_user():

    # Register a new user (admin only), make sure new username is unique write it to file
    users = open("user.txt", "a")

    # Allow only admin to register new users
    if user_name == "admin":
        # Request input of a new username, password, password confirmation
        new_username = input("Please enter a your username: ")

        while True:
            if new_username in user_dict:
                new_username = input("Username already in use, please input a different username: ")
            else:
                break

        new_password = input("Please enter a your password: ")
        confirm_password = input("Please re-enter your password for confirmation: ")

        # Check if the new password and confirmed password are the same, add to user text
        while True:
            if confirm_password == new_password:
                users.write(f"\n{new_username}, {new_password}")
                break
            else:
                confirm_password = input("Passwords not matching, please re-enter your password for confirmation: ")
    else:
        print("Only admin may register new users")

    users.close()
    return print("User successfully registered.")

def add_task():

    # Add a new task to the tasks.txt file
    task = open("tasks.txt", "a")

    # Ask the user for input on the task
    task_assign = input("The task is assigned to:  ")
    task_title = input("Enter task title: ")
    task_description = input("Enter task description: ")
    task_due_date = input("Enter task due date: (eg 10 December 2022): ")

    # Get current date and mark task as not yet completed
    today_date = date.today()
    task_set_date = today_date.strftime("%d %B %Y")
    task_complete = "No"

    task.write(f"\n{task_assign}, {task_title}, {task_description}, "
               f"{task_due_date}, {task_set_date}, {task_complete}")

    task.close()
    return print("Task successfully registered.")

def view_all():

    # View all tasks in the tasks.txt file, give a number identifier to each task
    view = open("tasks.txt", "r")
    view_tasks = view.readlines()

    for count, assignment in enumerate(view_tasks):
        assignment = assignment.split(", ")
        print(f'''Task No {count + 1}: 
    Task: \t\t\t\t{assignment[1]}
    Assigned to: \t\t{assignment[0]}
    Task Due Date: \t\t{assignment[3]}
    Task Set Date: \t\t{assignment[4]}
    Task Completed: \t{assignment[5]}
    Task Description: \t{assignment[2]}
    ''')

    view.close()
    return print("Tasks successfully viewed.")

def view_mine():

    # View only tasks assigned to the user logged in.
    # Return a list of the task numbers assigned to that user
    task_no = []
    for key in task_dict.keys():
        if user_name == task_dict[key][0]:
            task_no.append(key)
            print(f'''Task No {key}:
Task: \t\t\t\t{task_dict[key][1]}
Assigned to: \t\t{task_dict[key][0]}
Task Due Date: \t\t{task_dict[key][3]}
Task Set Date: \t\t{task_dict[key][4]}
Task Completed: \t{task_dict[key][5]}
Task Description: \t{task_dict[key][2]}
''')
    return task_no

def edit_mine(task_no):

    # Edit the tasks assigned to the current user and update task dictionary
    # User can mark complete, reassign to another user or update the due date

    select_task = int(input("Please enter a task number you would like to edit, or enter -1 for main menu: "))
    # Check the task entered belongs to the user, ask user what action to perform
    if select_task in task_no:
        action = input("Select an option:\n"
                       "m - mark complete\n"
                       "e - edit\n")
        if action == "m":
            task_dict[select_task][5] = "Yes"  # Change value in dictionary
            print(f"Task {select_task} now marked as complete!")

        # reassign user or edit due date
        if action == "e":
            if task_dict[select_task][5] != "Yes":
                action_edit = input("Select an option:\n"
                                    "re - reassign to different user\n"
                                    "dd - edit due date\n")
                if action_edit == "re":
                    reassign = input("Enter the username to reassign the task to: ")
                    task_dict[select_task][0] = reassign
                elif action_edit == "dd":
                    print(f"Current due date is: {task_dict[select_task][4]}")
                    due_date = input("Enter task due date (eg 10 Dec 2022): ")
                    task_dict[select_task][4] = due_date
            else:
                print("Task is already complete and cannot be edited")

    elif select_task not in task_no and select_task != -1:
        print(f"The task no. {select_task} does not belong to you")

    return print(f"The file tasks.txt has been updated!\n")

def view_stats():

    # Get the total number of tasks and the total number of users and return
    stats = open("tasks.txt", "r")
    stats_lines = stats.readlines()

    total_tasks = len(stats_lines)
    stats.close()

    quant_users = len(user_dict)

    return total_tasks, quant_users

def report_tasks(total_tasks):

    '''Create a report containing:
    total number of tasks, total complete tasks, total incomplete tasks, percentage of incomplete tasks
    number of incomplete tasks that are overdue, percentage of overdue tasks

    output the report to task_overview.txt'''

    # Check how many tasks are complete
    completed_tasks = 0
    incomplete_tasks = 0
    for value in task_dict.values():
        if value[5] == "Yes":
            completed_tasks += 1
        if value[5] == "No":
            incomplete_tasks += 1

    # Calculate percentage complete
    percent_incomplete = incomplete_tasks / total_tasks * 100
    percent_incomplete = round(percent_incomplete, 1)

    # Check if the tasks are overdue, set variables and current date
    present = datetime.now()
    pending_tasks = 0
    complete_tasks = 0
    overdue_tasks = 0

    # Convert date string to datetime value for comparison to current date
    for value in task_dict.values():
        due_date = value[3]
        task_due = datetime.strptime(due_date, "%d %B %Y")

        # If due date is 'smaller than' or 'before' today's date AND task is incomplete add to overdue tasks
        # elif add to complete tasks
        # else add to pending tasks
        if task_due.date() < present.date() and value[5] == "No":
            overdue_tasks += 1
            # print("Task Overdue")

        elif value[5] == "Yes":
            complete_tasks += 1
            # print("Task Complete")

        else:
            pending_tasks += 1
            # print("Not due yet")

    # Calculate percentage overdue
    percent_overdue = overdue_tasks / total_tasks * 100
    percent_overdue = round(percent_overdue, 1)

    # Write the results to file
    overview = open("task_overview.txt", "w")

    overview.write(f"The total number of tasks generated is_______________ {total_tasks}\n"
                   f"The total number of completed tasks is:______________ {completed_tasks}\n"
                   f"The total number on incomplete tasks is:_____________ {incomplete_tasks}\n"
                   f"The percentage of tasks that are incomplete is:______ {percent_incomplete}%\n"
                   f"The number of incomplete tasks that are overdue is:__ {overdue_tasks}\n"
                   f"The percentage of overdue tasks is:__________________ {percent_overdue}%")
    overview.close()

    return print("task_overview.txt has been updated")

def report_users():

    # Create a dictionary to hold data about each user
    # {user : [number of tasks, completed tasks, overdue tasks]}
    user_report = {}

    present = datetime.now()

    for user in user_dict:
        count_tasks = 0
        count_complete = 0
        count_overdue = 0

        for value in task_dict.values():

            due_date = value[3]
            task_due = datetime.strptime(due_date, "%d %B %Y")

            # If the first value matches the username
            if value[0] == user:
                count_tasks += 1
                user_report[user] = [count_tasks, count_complete, count_overdue]

                # If the last value is Yes the task is complete so add to total
                if value[5] == "Yes":
                    count_complete += 1
                    user_report[user] = [count_tasks, count_complete, count_overdue]

                # If the last value is no and due date past
                if task_due.date() < present.date() and value[5] == "No":
                    count_overdue += 1
                    user_report[user] = [count_tasks, count_complete, count_overdue]

    return user_report

def report_gen(report):

    # Generate report stats from the user report dictionary and output to file
    user_stats = view_stats()
    total_tasks = user_stats[0]

    user_overview = open("user_overview.txt", "w")

    for user in report:
        user_total_tasks = report[user][0]
        user_total_complete = report[user][1]
        user_total_overdue = report[user][2]

        user_perc_overall = round((user_total_tasks / total_tasks * 100), 2)
        user_perc_complete = round((user_total_complete / user_total_tasks * 100), 2)
        user_perc_incomplete = 100 - user_perc_complete
        user_perc_overdue = round((user_total_overdue / user_total_tasks * 100), 2)

        user_overview.write(f"{user}:\n"
    f"Total tasks assigned to {user}:_______________________________________{user_total_tasks}\n"
    f"Percentage of total tasks assigned to {user}:_________________________{user_perc_overall}%\n"
    f"Percentage of tasks assigned to {user} that are complete:_____________{user_total_complete}%\n"
    f"Percentage of tasks assigned to {user} that are incomplete:___________{user_perc_incomplete}%\n"
    f"Percentage of incomplete tasks assigned to {user} which are overdue:__{user_perc_overdue}%\n\n")

    user_overview.close()

    return print("user_overview.txt has been updated")

def call_reports():
    # Get the total tasks from get stats function
    user_stats = view_stats()
    total_tasks = user_stats[0]

    # Generate the task report and write it to file
    report_tasks(total_tasks)

    # Return the dictionary of {user : [number of tasks, completed tasks, overdue tasks]} store in 'report'
    report = report_users()

    # Generate report stats from the user report dictionary and output to file
    report_gen(report)

#====Dictionary of Users and Tasks====

# Create dictionary for each name and password {name:password}
user_dict = {}

users = open("user.txt", "r")
user_data = users.readlines()

# Read usernames and password from the user.txt file
# Store the data in dictionary {username : password}
for line in user_data:
    line = line.strip()
    login_data = line.split(", ")
    user_dict[login_data[0]] = login_data[1]

users.close()

# Create dictionary for each task {number: [task info as a list]}
task_dict = {}

user_tasks = open("tasks.txt", "r")
tasks = user_tasks.readlines()

for count, task in enumerate(tasks):
    task = task.strip()
    task = task.split(", ")
    task_dict[count + 1] = [task[0], task[1], task[2], task[3], task[4], task[5]]


#====Login Section====

# Ask for username and password and check against dictionary, if valid, grant access
user_name = input("Please enter your username: ")
user_password = input("Please enter your password: ")
access = user_login(user_name, user_password)

if access == True:
    print("Access Granted")


#====Perform Tasks Section====

while access == True:

    if user_name == "admin":
        # presenting the menu to admin
        # making sure that the user input is converted to lower case.
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    s - Display statistics
    gr - Generate reports
    e - Exit
    : ''').lower()
    else:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate reports
        e - Exit
        : ''').lower()

    # Register a new user
    if menu == "r":
        reg_user()

    # Add a new task
    elif menu == 'a':
        add_task()

    # View all tasks
    elif menu == 'va':
        view_all()

    # View only the tasks assigned to the user logged in
    elif menu == 'vm':
        # Print all tasks belonging to current user, return the list of task numbers associated with current user
        task_no = view_mine()

        # Edit the task content and update the dictionary
        edit_mine(task_no)

        # Print the updated dictionary values back to the tasks.txt
        update_tasks = open("tasks.txt", "w")

        update_lines = []                           # List to hold strings to write to file

        for value in task_dict.values():
            update_line = ""                        # String to put the dictionary values back into
            for item in value:
                update_line += item + ", "          # Add each item to the string including , space

            update_line = update_line[:-2]          # Remove the ", " from the end of each 'line'
            update_lines.append(update_line)

        # To avoid having a blank line at the end of the text file
        for count, line in enumerate(update_lines):
            if count < len(update_lines) - 1:
                update_tasks.write(f"{line}\n")
            else:
                update_tasks.write(f"{line}")

        update_tasks.close()

    # View the statistics (for admin only)
    elif menu == 's':

        # Check if the reports have already been generated (ie the files exist)
        tasks_exists = os.path.isfile("./task_overview.txt")
        users_exists = os.path.isfile("./user_overview.txt")

        # If they exist print the results to the terminal
        if tasks_exists == True and users_exists == True:

            stats_tasks = open("task_overview.txt", "r")
            print("Tasks Statistics:")
            print(f"{stats_tasks.read()}\n")
            stats_tasks.close()

            stats_users = open("user_overview.txt", "r")
            print("User Statistics:")
            print(f"{stats_users.read()}\n")
            stats_users.close()

        # If not generate the reports then print the results to the terminal
        else:
            call_reports()

            stats_tasks = open("task_overview.txt", "r")
            print("Tasks Statistics:")
            print(f"{stats_tasks.read()}\n")
            stats_tasks.close()

            stats_users = open("user_overview.txt", "r")
            print("User Statistics:")
            print(f"{stats_users.read()}\n")
            stats_users.close()

    elif menu == 'gr':

        call_reports()

    # Exit program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
