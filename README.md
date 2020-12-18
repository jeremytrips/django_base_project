# Base Project for Django
Django project that can be use to start a rest api based project. Each functionalities that have been implemented are so using dajngo-rest-framework.
The project create a custom user model and have the basics of user managment.
## Installation
Just download the repo and start working. 
You should consider to use a virtual environnement, below you just have a to open a command prompt (cmd) in the repo's folder.
```
py -m venv venvName
venvName\Scripts\activate
pip install -r req.txt
cd user_base
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
To check if the installation went well, go in your navigator at the following URL : http://127.0.0.1:8000/api/user/create/

## Usage

We suppose that you've some basic django and django rest-framework knowledge to use that projet. It's aim is just to save your time.

## Permission
As the authentication parameters have changed we have implemented new permissions:

- IsEmailVerified: Check wether the user have verified his email
- IsAccouneVisible: Check whether the user is in ghost mode. You may want to disbale some functionalities for those users.
- IsActive: That boolean is set to false when user decide to delete his account.
 
By default, for more security, the permission classes are:

- IsAuthenticated
- IsEmailVerified
- IsActive

You can always add or disable some in the settings.py file.
## Models

A few models have been created. Each of them is related to user registration or user reporting.

The first model is **CustomUser** model. It has the following fields
- email
- password
- first_name
- last_name
- is_admin
- is_staff
- is_active
- settings

That model is to be modified at your preference.

Another models that have been implemented is the **Settings** model.
It is used to store user settings and have the following boolean and is most likely te be modified
- allow_email_notification
- allow_push_notification
- is_email_verified
- account_is_visible

The account_is_visible is a boolean that is set to false when user want to delete his account. This is the default behavior of django as setting So you might provide a cron job that delete not account_is_visible users after a few weeks/months.

The settings models is linked to the user model with a OneToOne relationship.
The settings model can be accessed by:

```python
User.objects.get(email=foo).settings
```

The **ReportedUser**  models store users that missbehave on the platform. It is supposed to be created by another who want to report a behavior. 
- user_reporting
- user_reported 
- user_report_description


A last models that have been implemented is the **EmailVerificationToken**. You should not bother modifying it as it is created when the user is created and deleted when the user verify his account.

## Views
Views have been implemented to handle the basics.
|URL|Description| Response status if ok
---------- | ----|---------
```api/user/create/```|Register new user|HTTP_201_CREATED|
```api/user/delete/```|set ghost mode|HTTP_200_OK|
```api/user/login/```|Login user|HTTP_200_OK|
```api/user/logout/```|Logout user|HTTP_200_OK|
```api/user/verifytoken/```|Logout user|HTTP_200_OK|
```api/user/report/```|Report user|HTTP_201_CREATED|

### Create
Create a new user in the database.
1. Requiered field in header: 
 - Each field added in the CustomUser model
 - password2
2. Permissions needed
 - None
 
 url: ```api/user/create/```
 
 |Response status|Data returned|description|
 |-------------------|---------|----|
  |HTTP_201_CREATED|None|Register a new user
 |HTTP_206_PARTIAL_CONTENT|missing fields|Means that there is some missing data in the serializer.
 
 ### Delete
 Set the account_is_visible boolean to false in the Settings model coresponding to the user.
1. Requiered field in header: 
 - None
2. Permissions needed
 - IsEmailVerified

url: ```api/user/delete/```
  |Response status|Data returned|description|
 |-------------------|---------|----|
 |HTTP_200_OK|None|None

### Login
View used to login viewer
1. Requiered field in header: 
 - email
 - password
2. Permissions needed
 - None

url: ```api/user/login/```
|Response status|Data returned|description|
|-------------------|---------|----|
|HTTP_401_UNAUTHORIZED|["REGISTER_FIRST"]|User try to login with unknown credendtials.
|HTTP_401_UNAUTHORIZED|["VERIFY_EMAIL_FIRST"]|Email has not been verified yet.
|HTTP_401_UNAUTHORIZED|["USER_INACTIVE"]|User is inactive.
|HTTP_206_PARTIAL_CONTENT|serializer errors|Field missing in serializer.
|HTTP_200_OK|Authentication token| User is logged in.

### Logout
View used to login viewer
1. Requiered field in header: 
 - None
2. Permissions needed
 - IsAuthenticated

url: ```api/user/logout/```
|Response status|Data returned|description|
|-------------------|---------|----|
|HTTP_200_OK|None|User has logged out.

### Verify token
View used to login viewer
1. Requiered field in header: 
 - user_email
 - token
2. Permissions needed
 - none

url: ```api/user/verifytoken/```
|Response status|Data returned|description|
|-------------------|---------|----|
|HTTP_400_BAD_REQUEST|["DO_NOT_EXIST"]|User has not register.
|HTTP_400_BAD_REQUEST|["TOKEN_ERROR"]|Token furnished is wrong.
|HTTP_200_OK|None|Email user is verified.

### Report user
View used to report a user for his comportement.
1. Requiered field in header: 
 - reported_user (pk of the reported user)
 - reason
2. Permissions needed
 - none

url: ```api/user/report/```
|Response status|Data returned|description|
|-------------------|---------|----|
|HTTP_400_BAD_REQUEST|["REPORTED_USER_DOES_NOT_EXIST"]|reported user pk do not exist in db.
|HTTP_400_BAD_REQUEST|["REPORTED_USER_NOT_EMAIL_VERIFIED"]|Reported user is not email verified (nonsense).
|HTTP_400_BAD_REQUEST|["SELF_REPORT_NOT_ALLOWED"]|User try to report himself.
|HTTP_400_BAD_REQUEST|serializer errors|Missing data in serializer.
|HTTP_201_CREATED|None|Report has been created.

## Upcoming features

We plan on adding more user functionalities as:
- HTML templating email verification
- Improve admin panel
- user modification
