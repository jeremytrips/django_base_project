import io
import base_project.settings as s
import os
from django.core.files import File

file = File(open(os.path.join("static", "no_img.png"), "rb"))
file2 = File(open(os.path.join("static", "no_img.png"), "rb"))


serializer_create_correct_data = {
    "email": "jeremy.trips@tamere.com",
    "password": "pdcdezgf4545freff",
    "password2": "pdcdezgf4545freff",
    "home_address": "Zaventem",
    "studies": "Ingé de ouf",
    "first_name": "jeremy",
    "last_name": "Trips",
    "noma": "14122",
    "student_card": file
}


serializer_create_different_password_data = {
    "email": "jeremy.trips@tamere.com",
    "password": "pdf",
    "password2": "pdf2",
    "home_address": "Zaventem",
    "studies": "Ingé de ouf",
    "first_name": "jeremy",
    "last_name": "Trips",
    "noma": "14122",
    "student_card": file2
}

serializer_create_different_password_data = {
    "email": "jeremy.trips@tamere.com",
    "password": "pdf",
    "password2": "pdf",
    "home_address": "Zaventem",
    "studies": "Ingé de ouf",
    "first_name": "jeremy",
    "last_name": "Trips",
    "noma": "14122",
    "student_card": file2
}