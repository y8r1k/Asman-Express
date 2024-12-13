# forms.py
from django import forms
from .models import Expense, Issuance


class SearchForm(forms.Form):
    search_by = forms.ChoiceField(choices=[('client_id', 'ID клиента'), ('track_code', 'Трек-код')], required=True)
    client_id = forms.CharField(max_length=100, required=False)
    track_code = forms.CharField(max_length=255, required=False)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'comment']



class IssuanceForm(forms.ModelForm):
    class Meta:
        model = Issuance
        fields = ['total_weight', 'method_of_payment', 'comment']  # Убедитесь, что все нужные поля добавлены

    # Вы можете добавить дополнительные настройки для поля method_of_payment, если необходимо
    method_of_payment = forms.ChoiceField(
        choices=Issuance.MethodOfPayment.choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )