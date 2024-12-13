# forms.py
from django import forms
from .models import Expense


class SearchForm(forms.Form):
    search_by = forms.ChoiceField(choices=[('client_id', 'ID клиента'), ('track_code', 'Трек-код')])
    client_id = forms.CharField(max_length=100, required=False)
    track_code = forms.CharField(max_length=255, required=False)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'comment']
