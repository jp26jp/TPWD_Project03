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
    option = -1
    while option != 0:
        try:
            option = input("What would you like to do?\n\n[0]: Exit\n[1]: Add to timesheet\n[2]: Lookup task\n\n"
                           "Enter your choice: ")
            if int(option) == 0:
                break
            elif int(option) == 1:
                add_task()
            elif int(option) == 2:
                tasks = find_tasks()
                print_tasks(tasks)
            else:
                raise ValueError
        except ValueError:
            print("\nNot a valid option; enter 0, 1, or 2\n")


def add_task():
    """
    Adds a task to the timesheet
    """
    valid_int = False
    valid_date = False

    task_name = input("\nTask name: ")

    while not valid_int:
        try:
            task_time = input("Time spent on {}: ".format(task_name))
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
    file.write("{},{},{},{}\n".format(task.name, task.time_spent, task.notes, task.date))
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
        all_logs.append(Log(log["Name"], log["Time spent"], log["Notes"], log["Date"]))
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


def find_tasks() -> [Log]:
    """
    Provides a way for a user to find all of the tasks that were done on a certain date or that match a search string
    (either as a regular expression or a plain text search).

    :return: an array of found logs
    """
    file.close()
    query = input("\nEnter a date or search string: ")
    logs = rebuild_data()
    returned_tasks = []

    if is_date(query):
        for log in logs:
            if parse(query) == parse(log.date):
                returned_tasks.append(log)
    else:
        for log in logs:
            if re.search(r'{}'.format(query), log.name, re.I) \
                    or re.search(r'{}'.format(query), log.time_spent, re.I) \
                    or re.search(r'{}'.format(query), log.notes, re.I):
                returned_tasks.append(log)
    return returned_tasks


def print_tasks(tasks):
    """
    Prints a report of retrieved tasks to the screen, including the date, title of task, time spent, and general notes.

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
