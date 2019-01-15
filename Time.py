import csv
import re

from Log import Log
from dateutil.parser import parse

file = open("timesheet.csv", "w+")
file.write("Name,Time spent,Notes,Date\n")


def start():
    """
    Starts the program and asks user what they would like to do
    """
    while True:
        try:
            option = input(
                    "What would you like to do?\n\n"
                    "[0]: Exit\n"
                    "[1]: Add to timesheet\n"
                    "[2]: Lookup task\n\n"
                    "Enter your choice: ")
            if int(option) == 0:  # exit
                exit()
            elif int(option) == 1:  # add to timesheet
                add_to_timesheet()
            elif int(option) == 2:  # lookup task
                print_tasks(find_tasks())
            else:
                raise ValueError
        except ValueError:
            print("\nNot a valid option; enter 0, 1, or 2\n")


def add_to_timesheet():
    """
    Adds a task to the timesheet
    """
    valid_int = False
    valid_date = False

    task_name = input("\nTask name: ")

    while not valid_int:
        try:
            task_time = input("Minutes spent on {}: ".format(task_name))
            task_time = int(task_time)
            valid_int = True
        except ValueError:
            print("\nNot a valid time. Only enter numbers.\n")

    task_notes = input("Additional notes for {}: ".format(task_name))

    while not valid_date:
        try:
            task_date = input("Date of task (e.g. MM/DD/YYYY): ")
            task_date = parse(task_date)
            valid_date = True
        except ValueError:
            print("Not a valid date. Use format: MM/DD/YYYY")

    write_task_to_file(Log(task_name, task_time, task_notes, task_date))


def write_task_to_file(task):
    """
    Writes a task to the timesheet

    :param task: the task to be added to the timesheet
    """
    file.write("{},{},{},{}\n".format(task.name, task.time_spent, task.notes,
                                      task.date))
    print("\n{} has been added!\n".format(task.name))


def rebuild_data() -> [Log]:
    """
    Reads the data of the timesheet and converts it to an array of `Log`s

    :return: the logs in the timesheet
    """
    all_logs = []
    with open("./timesheet.csv", newline="") as csvFile:
        reader = csv.DictReader(csvFile, delimiter=",")
        logs = list(reader)
    for log in logs:
        all_logs.append(
                Log(log["Name"], log["Time spent"], log["Notes"], log["Date"]))
    return all_logs


def is_date(string) -> bool:
    """
    Verifies that a string is a date

    :param string: the string being verified
    :return: True or False
    """
    try:
        parse(string)
        return True
    except ValueError:
        return False


def get_input_search_method() -> int:
    while True:
        try:
            selection = input("\nEnter a search method.\n\n"
                              "[0]: find by date\n"
                              "[1]: find by time spent\n"
                              "[2]: find by exact search\n"
                              "[3]: find by pattern\n\n"
                              "Enter your choice: ")
            selection = int(selection)
            if selection == 0 \
                    or selection == 1 \
                    or selection == 2 \
                    or selection == 3:
                return selection
            else:
                raise ValueError
        except ValueError:
            print("\nNot a valid option; enter 0, 1, 2, or 3")


def get_input_date() -> str:
    while True:
        try:
            query = parse(input("\nEnter a date (e.g. MM/DD/YYYY): "))
            break
        except ValueError:
            print("\nNot a valid date (e.g. MM/DD/YYYY)")
    return str(query)


def get_input_time_spent() -> str:
    while True:
        try:
            query = int(input("\nEnter time spent in minutes: "))
            break
        except ValueError:
            print("\nNot a valid time. Only enter numbers.\n")
    return str(query)


def get_input_exact_search() -> str:
    return input("\nEnter a search query: ")


def get_task_by_pattern() -> str:
    return input("\nEnter a regex pattern: ")


def find_tasks() -> [Log]:
    """
    Provides a way for a user to find all of the tasks that were done on a
    certain date or that match a search string (either as a regular expression
    or a plain text search).

    :return: an array of found logs
    """
    file.close()
    logs = rebuild_data()
    returned_tasks = []

    input_search_method = get_input_search_method()

    if input_search_method == 0:
        query = get_input_date()
    elif input_search_method == 1:
        query = get_input_time_spent()
    elif input_search_method == 2:
        query = get_input_exact_search()
    elif input_search_method == 3:
        query = get_task_by_pattern()

    for log in logs:
        if input_search_method is 0:  # if true, query is a date
            if parse(query) == parse(log.date):
                returned_tasks.append(log)
        elif input_search_method is 1:  # if true, query is for time spent
            if int(query) == int(log.time_spent):
                returned_tasks.append(log)
        # if true, query is for exact match
        elif input_search_method is 2 or input_search_method is 3:
            if re.search(r'{}'.format(query), log.name) is not None \
                    or re.search(r'{}'.format(query), log.notes) is not None:
                returned_tasks.append(log)

    return returned_tasks


def print_tasks(tasks):
    """
    Prints a report of retrieved tasks to the screen, including the date,
    title of task, time spent, and general notes.

    :param tasks: tasks that were found
    """
    if len(tasks) == 0:
        print("\nNo tasks were found!")
    else:
        print("\nTasks found:")
        for task in tasks:
            print("Date: {}, Task name: {}, Time spent: {}, Notes: {}"
                  .format(task.date, task.name, task.time_spent, task.notes))
    exit()


if __name__ == '__main__':
    start()
