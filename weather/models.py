from tempfile import tempdir
from django.db import models

# Create your models here.
class Forecast:
    def __init__(self):
        self.day = ''
        self.date = ''
        self.icon = ''
        self.temp = ''
        self.feels_like = ''
        self.high = ''
        self.low = ''
        self.description = ''
        self.clouds = ''
        self.pop = ''