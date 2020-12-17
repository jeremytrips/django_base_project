# Base Project for Django

Django project that can be used to start a rest api based project. Each functionalities that have been implemented are using the django-rest-framework.

The project create a custom user model and has the basics of user managment. 

## Installation
There is no real installation needed as you should just download the repo and start working.

## Usage 
We suppose that you've some basic django and django rest-framework knowledge to use that projet. It's aim is just to save your time.

## Functionalities
We have created a new user model based on email password authentication. Default field are:
- email
- first_name
- last_name
- home_address
- birth_date
- description
- settings
- is_admin 
- is_staff 
- is_active
- settings

Settings represent the user settings:
- email notification
- push notification
- is_email_verified 
- account_is_visible

Field can surely be added in the user/models.py file

As the authentication parameters have changed we implemented new permissions:
- IsEmailVerified: Check whether the user has verified his email
- IsAccountVisible: Check whether the user is in ghost mode. You may want to disable some functionalities for those users.
- IsActive: That boolean is set to false when user decide to delete his account.

By default, for more security, the permission classes are:
- IsAuthenticated
- IsEmailVerified
- IsAccountVisible
- IsActive
You can always add or disable some in the settings.py file.
 
As we have said before, every functionalities has been implemented in a RESTful architecture. 
For now, user functionalities are:
- User registration
- User email verification
- User deleting
- User Login
- user Logout
- User reporting
- User inactive mode
- User settings model

## Upcoming features
We plan on adding more user functionalities as:
- HTML templating email verification
- Improve admin panel
