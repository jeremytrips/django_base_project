# django_base_projec

Django project that can be use to start a rest api based project. Each functionalities that have been implemented are so using dajngo-rest-framework.

The project create a custom user model and have the basics of user managment. 

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

As the authentication parameters have changed we have implemented new permissions:
- IsEmailVerified: Check wether the user have verified his email
- IsAccouneVisible: Check whether the user is in ghost mode. You may want to disbale some functionalities for those users.
- IsActive: That boolean is set to false when user decide to delete his account.

By default, for more security, the permission classes are:
- IsAuthenticated
- IsEmailVerified
- IsAccountVisible
- IsActive
You can always add or disable some in the settings.py file.
 
As we have said before every functionalities has been implemented in the FESTful architecture. 
For now user functionalities are:
- User registration
- User deleting
- User Login
- user Logout

## Upcoming features
We plan on adding more user functionalities as:
- User inactive mode
- User email verification
- User settings model
- User reporting
- ...

