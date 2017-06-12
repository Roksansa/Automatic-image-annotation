# -*- coding:utf-8 -*-
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
 
class ContactForm(forms.Form):
    image = forms.ImageField(label='Image', required=True)