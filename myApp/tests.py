from django.test import TestCase

# Create your tests here.
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.security import SecurityMiddleware
from django.middleware.common import CommonMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.middleware.clickjacking import XFrameOptionsMiddleware