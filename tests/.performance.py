#!/usr/bin/env python
# -*- coding: utf-8 -*-

from locust import HttpUser, task

class TestUser(HttpUser):
    @task
    def authenticate_task(self):
        self.client.get("/login")
        self.client.get("/register")
