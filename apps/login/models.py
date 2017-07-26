from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
# Create your models here.

NAME_REGEX = re.compile(r'^[a-zA-Z][0-9a-zA-Z .,-]*$')
class UserManager(models.Manager):

    def register(self, postData):
        results = {'register': True, 'error': [], 'user': None}
        if postData['first'] == '':
            results['register'] = False
            results['error'].append('Required First Name')
            #checks to see if the first name is not blank
        elif not NAME_REGEX.match(postData['first']):
            resutls['register'] = False
            results['error'].append('Not a Valid First Name')
            #implemented a name regex so that a user cannot input blank spaces as a name
        elif len(postData['first'])< 3:
            results['register'] = False
            results['error'].append('Name must be greater than 3 characters')
            #checks to make sure that the length of the sent field is at least 3 characters
        else:
            first_name = postData['first']
        if postData['last'] == '':
            results['register'] = False
            results['error'].append('Required Last Name')
            #same checks as first name
        elif not NAME_REGEX.match(postData['last']):
            results['register'] = False
            results['error'].append('Not a Valid Last Name')
        elif len(postData['last'])< 3:
            results['register'] = False
            results['error'].append('Name must be greater than 3 characters')
        else:
            last_name = postData['last']
        if postData['username'] == '':
            results['register'] = False
            results['error'].append('Username cannot be blank')
            #same checks as first name
        elif not NAME_REGEX.match(postData['username']):
            results['register'] = False
            results['error'].append('Not a Valid Username')
        elif len(postData['username'])< 3:
            results['register'] = False
            results['error'].append('Username must be greater than 3 characters')
        try:
            User.objects.get(username=postData['username'])
            results['register'] = False
            results['error'].append('Username already exists')
            #trys to grab the username supplied if it passes the get register is turned to false letting the user know that that username is already taken
        except:
            username = postData['username']
        if len(postData['pass1']) < 8:
            results['register'] = False
            results['error'].append('Password must be at least 8 characters')
            #checks to make sure that the length of the password is atleast 8 chracters
        elif postData['pass1'] != postData['pass2']:
            results['register'] = False
            results['error'].append('passwords do not match')
            #checks to see if the passwords match

        elif results['register']: #if the user has suppllied sufficient fields the user is then registered
            HashPass = postData['pass1']
            HashPass = HashPass.encode()

            hashedpass = bcrypt.hashpw(HashPass, bcrypt.gensalt())

            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, password=hashedpass)

            user.save()
            results['user']=user
        return results

    def login(self, postData):
        results = {'login':True, 'error': [], 'user':None}
        usernameTest = postData['usernameTest']
        try:
            user = User.objects.get(username=usernameTest)  #trys to grab the supplied username and matches with a supplied password
            password = postData['passTest']
            password = password.encode()
            test = user.password.encode()
            password = bcrypt.hashpw(password, test)
            if password == user.password:
                results['register'] = True
                results['user']=user
                return results
            else:
                results['login'] = False
                results['error'].append('Incorrect Username/Password Combination')
                return results
        except:
            results['login'] = False
            results['error'].append('Incorrect Username/Password Combination')
            return results
            #both of the errors are the same to prevent a potential hacker from finding a correct username or password reducing the amount of time required to hack into the site

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
