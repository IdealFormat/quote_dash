from django.db import models
from datetime import datetime
import re, bcrypt
from django.utils.translation import check_for_language
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long."
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters."
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match."
        if len(postData['email']) < 1:
            errors['reg_email'] = "Email address cannot be blank."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Please enter a valid email address."
        elif check:
            errors['reg_email'] = "Email address is already registered."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors

    def update_validator(self, postData):
        errors  = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name cannot be blank."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name cannot be blank."
        if len(postData['email']) < 1:
            errors['reg_email'] = "Email address cannot be blank."
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors['reg_email'] = "Please enter a valid email address."
        return errors

    def quote_validator(self, postData):
        errors  = {}
        if len(postData['quote_author']) < 3:
            errors['quote_author'] = "Author must be more than 3 characters."
        if len(postData['quote']) < 10:
            errors['quote'] = "Quote must be at least 10 characters long"
        return errors

        
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    quote_author = models.CharField(max_length=50, default="NULL")
    quote = models.CharField(max_length=255)
    user_quote = models.ForeignKey(User, related_name='quotes', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_quotes')