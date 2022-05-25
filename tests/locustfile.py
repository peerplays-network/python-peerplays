import time
from locust import HttpUser, task, between
from fixtures import peerplays

class QuickstartUser(HttpUser):
    # wait_time = between(1, 5)

    @task(3)
    def posts_albums(self):
        # info = peerplays.info()
        # print("info:", info)
        # self.client.get("/posts")
        # self.client.get("/albums")
        pass

    @task(3)
    def view_todos(self):
        # for user_id in range(10):
            # self.client.get(f”/todos?userId={user_id}“, name=“/todos”)
            # self.client.get("/todos/1") # , name="/todos")
            # print("a:", a)
        info = peerplays.info()
        # print("info:", info)
        self.client.get("/todos/1") #, name="/todos")
            # print ("Testing loop:", user_id)
        # time.sleep(0.02)

    def on_start(self):
        # info = peerplays.info()
        # print("info:", info)
        pass
        # self.client.post("/login", json={"username":"foo", "password":"bar"})
