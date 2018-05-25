from django.db import models
import bcrypt
import re

# Create your models hereself.

class UserManager(models.Manager):
    def register_user(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        response = {
            "errors": []
        }
        if len(User.objects.filter(email=postData['email'])) > 0 :
            response["errors"].append("Username entered is already registered on this site.")
        if len(postData['first_name']) < 2:
            response["errors"].append("Your name is required to be at least 2 characters.")
        if len(postData['last_name']) < 2:
            response["errors"].append("User name is required to be at least 2 characters.")
        if len(postData['password']) < 1:
            response["errors"].append("Password field can not be empty.")
        if len(postData['password']) < 8:
            response["errors"].append("Password be at least 8 characters.")
        if postData["password"] != postData["confirm"]:
            response["errors"].append("Confirmation password and password do not match.")
        if not EMAIL_REGEX.match(postData['email']):
            response["errors"].append("Please enter a valid email address.")
        if not NAME_REGEX.match(postData['first_name']):
            response["errors"].append("Your first name can not contain a number.")
        if not NAME_REGEX.match(postData['last_name']):
            response["errors"].append("Your last name can not contain a number.")
        #checking if user is in database
        if len(response["errors"]) == 0:
            user = User.objects.create(first_name=postData["first_name"], last_name=postData["last_name"], email=postData["email"], password=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()).decode('utf-8'))
            user.save()
            response["user_id"] = user.id
        return response

    def login_user(self, postData):
        response = {
            "errors": []
        }
        user = User.objects.filter(email=postData['email'])
        if len(user) < 1: #user is not registered
            response["errors"].append("Please Register for the site first.")
        else:
            user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                response["user_id"] = user.id
            else:
                response["errors"].append("User Account, and password combination did not match.")
        return response


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

# class Facebook_User(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     fb_id = models.CharField(max_length=255)

class Post(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Comment(models.Model):
    post_id = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
