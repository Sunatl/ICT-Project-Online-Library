from django import forms
from .models import *

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
        fields = ['book', 'quantity','grade']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Шумораи китоб'}),
        }
from django import forms
from .models import Book, Grade

class ClassBookSelectForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Шумораи китоб'})
    )

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'purchase', 'amount_paid', 'status']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'purchase': forms.Select(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Маблағи пардохт'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'phone_number', 'date', 'books']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номи мактаб'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Нақшаи мактаб'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Рақами телефон'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Таърихи таъсисёбӣ'}),
            'books': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class StudentBookForm(forms.ModelForm):
    class Meta:
        model = StudentBook
        fields = ['student', 'book', 'quantity', 'school']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Шумораи китоб'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }
