from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name is too Short!"
        if postData['first_name'].isalpha() == False:
            errors['fname_alpha'] = "First name can only contain letters!"


        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name is too Short!"
        if postData['last_name'].isalpha() == False:
            errors['lname_alpha'] = "Last name can only contain letters!"

        if len(postData['email']) < 5:
            errors['email'] = "Email is too Short!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not  EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Not a valid email address!"
        match = User.objects.filter(email=postData['email'])
        if len(match) > 0:
            errors['exists'] = "This account already exists!"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too Short!"
        if postData['password'] != postData['password_conf']:
            errors['match'] = "Passwords do not match"
        return errors

class BookManager(models.Manager):
    def create_book_validator(self, postData):
        errors = {}
        match = Book.objects.filter(title=postData['title'])
        if len(postData['title']) < 2:
            errors['title'] = "Book title must be at least 2 characters"
        if len(postData['description']) < 5:
            errors['desc'] = "Description must be at least 5 characters"
        if len(match) > 0:
            errors['exists'] = "This Book already exists"
        return errors
    
    def update_book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Book title must be at least 2 characters"
        if len(postData['description']) < 5:
            errors['desc'] = "Description must be at least 5 characters"
        return errors





class User(models.Model):
    first_name = models.CharField(max_length= 45)
    last_name = models.CharField(max_length= 45)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length= 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length= 255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    objects = BookManager()
