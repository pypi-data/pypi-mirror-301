from .inhouse_api import InhouseAPI
import pwinput
import argparse
from sys import exit
from . import utils

__version__ = "0.1.0"
__author__ = "NurTasin"

api = InhouseAPI()

def loginFunc(args):
    if(args.email is None):
        args.email = input("Email: ")
    if(args.password is None):
        args.password = pwinput.pwinput(prompt="Password: ", mask="*")
    try:
        loginData = api.login(args.email, args.password)
    except Exception as e:
        print(f"[ERROR] {e}")
    if(api.isLoggedIn()):
        print("[LOG] Logged in successfully")
        userData = api.getUserData()
        print(f"Welcome, {userData['name']} ({loginData['user']['email']})")
    else:
        print("[ERROR] Login failed")
        exit(1)

def getMyDataFunc(args):
    try:
        userData = api.getUserData()
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)
    if userData:
        print(f"Name: {userData['name']}\nID: {userData['user_id']}")
    else:
        print("[ERROR] Something went wrong")
        exit(1)

def listFunc(args):
    if(args.type == "projects"):
        projects = api.getProjects()
        if projects:
            print(utils.renderProjectsTable(projects).draw())
        else:
            print("[ERROR] Something went wrong")
            exit(1)
    elif(args.type == "tasks"):
        tasks = api.getTaskOverview()
        args.category = args.category or "ongoing"
        if tasks:
            print(utils.renderTasksTable(tasks, args.category).draw())
        else:
            print("[ERROR] Something went wrong")
            exit(1)
    elif(args.type == "users"):
        users = api.getUsers()
        if users:
            print(utils.renderUsersTable(users).draw())
        else:
            print("[ERROR] Something went wrong")
            exit(1)
    elif(args.type == "plans"):
        plans = api.getTodaysPlan()
        if plans:
            print(utils.renderTodaysPlanTable(plans).draw())
        else:
            print("[ERROR] Something went wrong")
            exit(1)
    else:
        print(f"[ERROR] {args.type} is not a valid type")
        exit(1)

def createTaskFunc(args):
    if args.pid is None:
        args.pid = input("Project ID: ")
    if args.due is None:
        args.due = input("Due Date (YYYY-MM-DD): ")
    if args.res is None:
        args.res = input("Resources (empty for none): ")
    if args.desc is None:
        args.desc = input("Description (empty for none): ")
    
    print("Now enter task names one by one (enter #end to finish)")
    tasks = []
    while True:
        task = input("Task Name: ")
        if task == "#end":
            break
        elif task.strip() == "":
            print("Task name cannot be empty")
        else:
            tasks.append(task)
    try:
        res = api.createTasks(args.pid, tasks, args.due, args.res, args.desc)
        if res:
            print("[SUCCESS] Task creation successful")
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)

def markActiveFunc(args):
    try:
        res = api.makeTaskActive(args.tids, args.category)
        if res:
            print("[SUCCESS] Task activation successful. Task(s) are in \"incomplete\" state")
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)

def markOngoingFunc(args):
    try:
        res = api.markTasksOngoing(args.tids)
        if res:
            print("[SUCCESS] Task(s) marked \"ongoing\"")
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)

def markDoneFunc(args):
    try:
        res = api.markTasksComplete(args.tids)
        if res:
            print("[SUCCESS] Task(s) marked \"complete\"")
    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)


def aboutFunc(args):
    print(r"""
$$\   $$\                        $$\                    $$$$$$\  $$\       $$$$$$\ 
$$ | $$  |                       $$ |                  $$  __$$\ $$ |      \_$$  _|
$$ |$$  / $$$$$$\  $$$$$$\$$$$\  $$ | $$$$$$\          $$ /  \__|$$ |        $$ |  
$$$$$  /  \____$$\ $$  _$$  _$$\ $$ | \____$$\ $$$$$$\ $$ |      $$ |        $$ |  
$$  $$<   $$$$$$$ |$$ / $$ / $$ |$$ | $$$$$$$ |\______|$$ |      $$ |        $$ |  
$$ |\$$\ $$  __$$ |$$ | $$ | $$ |$$ |$$  __$$ |        $$ |  $$\ $$ |        $$ |  
$$ | \$$\\$$$$$$$ |$$ | $$ | $$ |$$ |\$$$$$$$ |        \$$$$$$  |$$$$$$$$\ $$$$$$\ 
\__|  \__|\_______|\__| \__| \__|\__| \_______|         \______/ \________|\______|
                                                                                   
""")
    print(f"kamla-cli v{__version__}")
    print(f"Author: {__author__}")

parser = argparse.ArgumentParser(prog="kamla-cli",description="Inhouse Ten CLI")
parser.add_argument("--version","-v", action="version", version=f"kamla-cli v{__version__}")
commandParser = parser.add_subparsers(dest="command", required=True, help="sub-command help")

login = commandParser.add_parser("login", help="Login to Inhouse")
login.add_argument("--email", help="Email", required= False)
login.add_argument("--password", help="Password", required= False)
login.set_defaults(func=loginFunc)

getMe = commandParser.add_parser("me", help="Get user data")
getMe.set_defaults(func=getMyDataFunc)

listParser = commandParser.add_parser("list", help="List projects and tasks")
listParser.add_argument("type", help="Type of list", choices=["projects", "tasks", "users", "plans"])
listParser.add_argument("-C", "--category", help="Category filter (only for `list tasks`)")
listParser.set_defaults(func=listFunc)

createTask = commandParser.add_parser("create", help="Create a task")
createTask.add_argument("--pid", help="Project ID")
createTask.add_argument("--due", help="Due Date")
createTask.add_argument("--res", help="Resources")
createTask.add_argument("--desc", help="Description")
createTask.set_defaults(func=createTaskFunc)

# Mark command with subcommands
markCommand = commandParser.add_parser("mark", help="Marks task(s) to a given status")
markSubcommands = markCommand.add_subparsers(dest="markType", required=True, help="Mark type sub-commands")

# Mark active subcommand
markActive = markSubcommands.add_parser("active", help="Mark task(s) as active")
markActive.add_argument("tids", help="Task ids that you want to make active (comma separated)")
markActive.add_argument("category", help="Category of the task(s)")
markActive.set_defaults(func=markActiveFunc)

# Mark ongoing subcommand
markOngoing = markSubcommands.add_parser("ongoing", help="Mark task(s) as ongoing")
markOngoing.add_argument("tids", help="Task ids that you want to make ongoing (comma separated)")
markOngoing.set_defaults(func=markOngoingFunc)

# Mark done subcommand

markDone = markSubcommands.add_parser("done", help="Mark task(s) as completed")
markDone.add_argument("tids", help="Task ids that you want to make completed (comma separated)")
markDone.set_defaults(func=markDoneFunc)

aboutParser = commandParser.add_parser("about", help="About the CLI")
aboutParser.set_defaults(func=aboutFunc)

def main():
    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__=="__main__":
    main()
