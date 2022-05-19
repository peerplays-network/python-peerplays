#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from locust import HttpUser, task, between

class AuthenticateUser(HttpUser):
    timer = between(1, 10)

    @task
    def authenticate_task(self):
        self.client.get("/login")
        self.client.get("/register")

    def on_start(self):
        self.client.post("/register", json={"username":"testuser", 
                                            "email":"test@test.com", 
                                            "password":"password"})
