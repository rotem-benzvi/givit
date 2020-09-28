from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

MEMBERSHIP_TYPE = [
    ('friend', 'friend'),
    ('coordinator', 'coordinator'),
]

DEGREE = [
    ('BA', 'BA'),
    ('BSC', 'BSC'),
    ('MA', 'MA'),
    ('MSC', 'MSC'),
    ('PHD', 'PHD'),
]

FIELD_OF_STUDY = [
    ('Computer Science', 'Computer Science'),
    ('Business', 'Business'),
    ('Sustainability', 'Sustainability'),
    ('Communications', 'Communications'),
    ('Economics', 'Economics'),
    ('Law', 'Law'),
    ('Psychology', 'Communications'),
    ('Government, Diplomacy and Strategy',
     'Government, Diplomacy and Strategy'),
]

GENDER = [
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other'),
]


class Profile(models.Model):

    phone_regex = RegexValidator(
        regex=r'^05[0-68-9][0-9]{7}$',
        message="Phone number must be entered in the format: 05XXXXXXXX.")
    id_regex = RegexValidator(
        regex=r'\d{8,9}', message="ID must be 9 digits long.")
    house_number_regex = RegexValidator(
        regex=r'\d{1,3}', message="Please enter a valid number from 1 to 999.")

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    confirmed = models.BooleanField("confirmed", default=False)
    student_id = models.CharField(max_length=10, validators=[id_regex])
    gender = models.CharField(max_length=10, default='other', choices=GENDER)
    phone_number = models.CharField(max_length=10, validators=[phone_regex])
    date_of_birth = models.DateField(max_length=8)
    address_street_name = models.CharField(
        max_length=50, verbose_name='street')
    address_house_number = models.CharField(
        max_length=3, verbose_name='home_number',
        validators=[house_number_regex])
    address_city = models.CharField(max_length=50, verbose_name='city')
    field_of_study = models.CharField(
        max_length=100, default='Computer Science', choices=FIELD_OF_STUDY)
    degree = models.CharField(max_length=100, default='BA', choices=DEGREE)
    scholarship = models.CharField(max_length=100)
    membership_type = models.CharField(
        max_length=100, default='friend', choices=MEMBERSHIP_TYPE)

    def _str_(self):
        return self.user.username
