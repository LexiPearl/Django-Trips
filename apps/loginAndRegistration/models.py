from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]*$')

class UserManager(models.Manager):
    def UserValidator(self, postData):
        flag=False
        errors=[]
        if len(postData['name']) < 3:
            errors.append("Name must be at least 3 characters!")
            flag=True
        elif not NAME_REGEX.match(postData['name']):
            errors.append("Invalid name!")
            flat=True
        if len(postData['username']) <3:
            flag=True
            errors.append("Username must be at least 3 characters!")
        if len(postData['password'])<8:
            flag=True
            errors.append("Password length is invalid")
        if len(postData['password_confirmation']) < 1:
            errors.append("Confirm password cannot be empty!")
            flag=True
        if postData['password_confirmation'] != postData['password']:
            flag=True
            errors.append("Passwords do not match!")
        if not flag:
            pwhash= bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt())
            User.objects.create(
                name=postData['name'],
                username=postData['username'],
                password= pwhash )
            user = User.objects.last()
            return (flag, user)
        return (flag, errors)
    def userLogin(self, postData):
        login= User.objects.filter(username=postData['username'])
        if len(login)<1:
            return (False, "User does not exist in database")
        else:
            user= User.objects.get(username=postData['username'])
            password= postData['password'].encode()
            hashed=user.password.encode()
            if bcrypt.hashpw(password, hashed )== hashed and user:
                return (True, user)
            else:
                return (False, "Username and password do not match")

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()
