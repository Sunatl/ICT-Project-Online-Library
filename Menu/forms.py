from django import forms
from .models import *  # Импорт кардани тамоми моделҳо

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номи синф'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Тавсифи иловагӣ'}),
        }

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance']
        widgets = {
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Баланс'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'stock', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номи китоб'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Тавсифи китоб'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Нарх'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Шумораи саҳом'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [ 'book', 'quantity']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Шумораи китоб'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method','purchase','amount_paid','status']  # Роҳи пардохт


