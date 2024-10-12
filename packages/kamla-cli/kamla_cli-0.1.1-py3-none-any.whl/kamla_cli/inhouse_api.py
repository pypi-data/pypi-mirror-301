import requests as req
import json
import os
from . import utils

class InhouseAPI:
    BASE_URL = "https://inhouse-api.ongshak.com"
    def __init__(self):
        self.http = req.Session()
        self.accessToken = None
        self.refreshToken = None
        self.uid = None
    
    def isLoggedIn(self):
        return not (self.accessToken is None) and not(self.refreshToken is None)

    def login(self, email, password):
        res = self.http.post(f"{self.BASE_URL}/rest-auth/login/",json={
            "email": email,
            "password": password
        })
        if(res.status_code == 400):
            raise Exception("Invalid email or password")
        elif(res.status_code != 200):
            raise Exception("Something went wrong")
        
        data = res.json()
        self.setTokens(
            data["access"],
            data["refresh"]
        )
        self.uid = data["user"]["pk"]
        if self._dumpTokens():
            print("[LOG] Session Stored")
        return data
    

    def setTokens(self, accessToken, refreshToken):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
    
    def getTokens(self):
        if(self.accessToken is None or self.refreshToken is None):
            raise Exception("Tokens are not set")
        return {"access":self.accessToken, "refresh":self.refreshToken}
    
    def _dumpTokens(self):
        if(self.accessToken is None or self.refreshToken is None):
            raise Exception("Tokens are not set")
        
        APP_DIR = os.path.expanduser("~")
        with open(os.path.join(APP_DIR,".kamla-session.json"), "w+") as f:
            json.dump({
                "access": self.accessToken,
                "refresh": self.refreshToken
            }, f)
            return True
    
    def loadTokens(self):
        APP_DIR = os.path.expanduser("~")
        sessionPath = os.path.join(APP_DIR,".kamla-session.json")

        if(os.path.exists(sessionPath)):
            with open(sessionPath, "r") as f:
                data = json.load(f)
            self.setTokens(data["access"], data["refresh"])
            test = self.http.get(f"{self.BASE_URL}/users/get_profile/",
                            headers={"Authorization": f"Bearer {self.accessToken}"})
            if test.status_code == 401 :
                if test.json()['code']=="token_not_valid":
                    print("[ERROR] Token expired! Please login again")
                    self.accessToken = None
                    self.refreshToken = None
                    os.remove(sessionPath)
                    return False
                else:
                    print("[ERROR] Something went wrong")
                    return False
            else:
                self.uid = test.json()["user_id"]
                return True

        return False
    
    def sessionPrecheck(self):
        if(self.isLoggedIn() == False):
            if self.loadTokens() == False :
                print("[ERROR] No logged in session found. try 'kamla-cli login'")
                exit(1)

    def getUserData(self):
        self.sessionPrecheck()
        res = self.http.get(f"{self.BASE_URL}/users/get_profile/",
                            headers={"Authorization": f"Bearer {self.accessToken}"})
        if(res.status_code != 200):
            raise Exception("Something went wrong")
        
        data = res.json()
        return data
    
    def getTaskOverview(self):
        self.sessionPrecheck()
        res = self.http.get(f"{self.BASE_URL}/projects/task_overview/", headers={
            "Authorization": f"Bearer {self.accessToken}"
        })
        if(res.status_code != 200):
            raise Exception("Something went wrong")
        
        data = res.json()
        return data
    
    def getProjects(self):
        self.sessionPrecheck()
        res = self.http.get(f"{self.BASE_URL}/projects/add_task/",
                headers={
                    "Authorization": f"Bearer {self.accessToken}"
                })
        if(res.status_code != 200):
            raise Exception("Something went wrong")
        
        data = res.json()["projects"]
        return data
    
    def getUsers(self):
        self.sessionPrecheck()
        res = self.http.get(f"{self.BASE_URL}/projects/add_task/",
                headers={
                    "Authorization": f"Bearer {self.accessToken}"
                })
        if(res.status_code != 200):
            raise Exception("Something went wrong")
        
        data = res.json()["users"]
        return data
    
    def getTodaysPlan(self):
        self.sessionPrecheck()
        res = self.http.get(f"{self.BASE_URL}/projects/todays_plan/",
                headers={
                    "Authorization": f"Bearer {self.accessToken}"
                })
        if(res.status_code != 200):
            raise Exception("Something went wrong")
        
        data = res.json()
        return data
    
    def createTasks(self, project_id, tasks, due_date, resources, description):
        self.sessionPrecheck()
        res = self.http.post(f"{self.BASE_URL}/projects/add_task/",
                headers={
                    "Authorization": f"Bearer {self.accessToken}"
                },
                json={
                    "project_id": project_id,
                    "user_id": self.uid,
                    "task_names": tasks,
                    "resources": resources,
                    "description": description,
                    "due_date": due_date
                })
        if(res.status_code != 200):
            raise Exception("[ERROR] Task creation failed. The server responded with status code " + str(res.status_code))
        
        data = res.json()
        return data
    
    def makeTaskActive(self, taskIds, category):
        self.sessionPrecheck()
        taskIds = [int(x.strip()) for x in taskIds.split(",")]
        if not category in utils.categoryToSlug.keys():
            raise Exception(f"Invalid category {category}. Valid categories are {', '.join(utils.categoryToSlug.keys())}")
        payload = [
            {
                "task_id": taskId,
                "category": utils.categoryToSlug[category]
            } for taskId in taskIds
        ] 
        res = self.http.post(f"{self.BASE_URL}/projects/todays_plan/",
                headers={
                    "Authorization": f"Bearer {self.accessToken}"
                },
                json=payload)
        if(res.status_code != 200):
            raise Exception("[ERROR] Task activation failed. The server responded with status code " + str(res.status_code))
        
        data = res.json()
        return data
    
    def markTasksOngoing(self, taskIds):
        self.sessionPrecheck()
        taskIds = [int(x.strip()) for x in taskIds.split(",")]
        payload = [
            {
                "task_id": taskId,
                "status": "ongoing"
            } for taskId in taskIds
        ] 
        res = self.http.post(f"{self.BASE_URL}/projects/task_overview/",
                headers={
                    "Authorization": f"Bearer {self.accessToken}"
                },
                json=payload)
        if(res.status_code != 200):
            raise Exception("[ERROR] Task marking ongoing failed. The server responded with status code " + str(res.status_code))
        
        data = res.json()
        return data
    
    def markTasksComplete(self, taskIds):
        self.sessionPrecheck()
        taskIds = [int(x.strip()) for x in taskIds.split(",")]
        payload = [
            {
                "task_id": taskId,
                "status": "completed"
            } for taskId in taskIds
        ] 
        res = self.http.post(f"{self.BASE_URL}/projects/task_overview/",
                headers={
                    "Authorization": f"Bearer {self.accessToken}"
                },
                json=payload)
        if(res.status_code != 200):
            raise Exception("[ERROR] Task marking ongoing failed. The server responded with status code " + str(res.status_code))
        
        data = res.json()
        return data

