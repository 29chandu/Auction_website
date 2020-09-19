from django.forms import ModelForm
from django import forms

from django.core.validators import MinValueValidator, MaxValueValidator

import decimal

from . import models

class ListingForm(ModelForm):
    class Meta:
        model = models.Listing
        fields = [
            'title',
            'description',
            'image',
            'start_bid',
            'category'
        ]


class BidForm(forms.Form):
    current_bid = forms.DecimalField(max_digits=10, decimal_places=2, min_value=decimal.Decimal('0.01'))


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=255, strip=True,
    widget=forms.TextInput(attrs={'placehoder':'Comment'}))