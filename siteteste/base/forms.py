from dataclasses import fields
from django.forms import ModelForm
from .models import Room

# fazer o html automatico de acordo com os fiels do model de rooms
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'