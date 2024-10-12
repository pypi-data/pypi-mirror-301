from texttable import Texttable
from datetime import datetime
import pytz

slugToCategory = {
    "important_urgent": "UI",
    "important_not_urgent": "!UI",
    "not_important_urgent": "U!I",
    "not_important_not_urgent": "!U!I"
}

categoryToSlug = {
    "UI": "important_urgent",
    "IU": "important_urgent",
    "!UI": "important_not_urgent",
    "I!U": "important_not_urgent",
    "U!I": "not_important_urgent",
    "!IU": "not_important_urgent",
    "!U!I": "not_important_not_urgent",
    "!I!U": "not_important_not_urgent"
}

def parseCategory(category,key = "ongoing"):
    data = []
    for projects in category[key].keys():
        for task in category[key][projects]:
            data.append([
                task["get_assigned_user"]["name"],
                slugToCategory[task["category"]],
                task["project_name"] + " - #" + str(task["project"]),
                "#"+str(task["id"]),
                task["task_name"],
                key,
                getFormattedDateTime(task["date_added"])
            ])
    
    return data


def renderTasksTable(data, category = "ongoing"):
    table = Texttable()
    table.set_cols_align(["c", "c", "c", "c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m", "m"])
    table.set_max_width(100)

    if category == "all":
        category = "ongoing,completed,incomplete"
    category = [x.strip() for x in category.split(",")]

    all_rows = [["User", "Category", "Project", "Task ID", "Task Name", "Status", "Added On"]]  # Start with headers

    for user in data:
        for cat in category:
            important_urgent = parseCategory(user["important_urgent"], cat)
            important_not_urgent = parseCategory(user["important_not_urgent"], cat)
            not_important_urgent = parseCategory(user["not_important_urgent"], cat)
            not_important_not_urgent = parseCategory(user["not_important_not_urgent"], cat)

            # Add all parsed categories to the all_rows list
            all_rows.extend(important_urgent)
            all_rows.extend(important_not_urgent)
            all_rows.extend(not_important_urgent)
            all_rows.extend(not_important_not_urgent)

    table.add_rows(all_rows)  # Add headers and data at once

    return table

def renderProjectsTable(data):
    table = Texttable()
    table.set_cols_align(["c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m"])
    table.set_max_width(90)
    all_rows = [["ID", "Name", "Status", "Added On"]]
    for project in data:
        all_rows.append([
            project["id"],
            project["name"],
            project["status"],
            project["created_on"]
        ])
    table.add_rows(all_rows)
    return table

def renderUsersTable(data):
    table = Texttable()
    table.set_cols_align(["c", "c"])
    table.set_cols_valign(["m", "m"])
    table.set_max_width(40)
    all_rows = [["ID", "Name"]]
    for user in data:
        all_rows.append([
            user["user_id"],
            user["name"]
        ])
    table.add_rows(all_rows)
    return table

def renderTodaysPlanTable(data):
    data.sort(key=lambda x: x['id'], reverse=False)
    table = Texttable()
    all_rows = [["Project", "Task ID", "Task Name", "Due Time"]]
    table.set_cols_align(["c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m"])
    table.set_max_width(90)
    for task in data:
        all_rows.append([
                task["project_name"],
                task["id"],
                task["task_name"],
                getFormattedDateTime(task["due_date"])
            ])
    table.add_rows(all_rows)
    return table

def getFormattedDateTime(utc_str):
    try:
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except Exception as e:
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
    local_tz = pytz.timezone('Asia/Dhaka')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    formatted_date = local_dt.strftime("%d-%m-%Y\n%H:%M")
    return formatted_date

