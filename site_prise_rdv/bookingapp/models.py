from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms


TIME_CHOICES = (
    ("9 AM", "9 AM"),
    ("10 AM", "10 AM"),
    ("11 AM", "11 AM"),
    ("1:30 PM", "1:30 PM"),
    ("2:30 PM", "2:30 PM"),
    ("3:30 PM", "3:30 PM"),
  
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default=("9 AM"))
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    notes = models.TextField(blank=True)
    motif = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"

class NoteForm(forms.Form):
    notes = forms.CharField(widget=forms.Textarea)
