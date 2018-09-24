from django.db import models
from django.contrib import messages
import re
import bcrypt


class Manager(models.Manager):

    def validate_reg(self, data):

        errors = {}
        emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data["first_name"]) < 1:
            errors["first_name"] = "Please enter a first name"
        elif not data["first_name"].isalpha():
            errors["first_name"] = "Names may only contain letters"

        if len(data["last_name"]) < 1:
            errors["last_name"] = "Please enter a last name"
        elif not data["last_name"].isalpha():
            errors["last_name"] = "Names may only contain letters"

        if len(data["email"]) < 1:
            errors["email"] = "Please enter an Email Address"
        elif not emailRegEx.match(data["email"]):
            errors["email"] = "You must enter a valid Email Address"

        already_reg = User.objects.filter(email=data["email"])
        if already_reg:
            errors["email"] = "You are already registered with this Email Address"

        if len(data["password"]) < 1:
            errors["password"] = "Please enter a password"
        elif len(data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters"

        if len(data["confirm_password"]) < 1:
            errors["confirm_password"] = "Please confirm your password"
        elif data["confirm_password"] != data["password"]:
            errors["password"] = "Your passwords must match"
            errors["confirm_password"] = "Your passwords must match"

        return errors

    def validate_login(self, data):

        errors = []
        emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data["email"]) < 1:
            errors.append("Please enter an Email Address")
        elif not emailRegEx.match(data["email"]):
            errors.append("You must enter a valid Email Address")

        if len(data["password"]) < 2:
            errors.append("Please enter a password")

        if errors: 
            return [errors, 0]

        user = User.objects.filter(email=data["email"])
        
        if user: 
            user = user[0]
            if not bcrypt.checkpw(data["password"].encode(), user.password.encode()):
                errors.append("Failed to log in, check your email and password")
        else:
            errors.append("Failed to log in, check your email and password")

        context = {
            "id" : user.id,
            "first_name" : user.first_name,
            "last_name" : user.last_name,
            "created_at" : user.created_at
        }
        return [errors, context]





class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()


class Wish(models.Model):
    user = models.ForeignKey(User, related_name="wishes", on_delete=models.CASCADE)
    wish = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    granted = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    wish = models.ForeignKey(Wish, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)