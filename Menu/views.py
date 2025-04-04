from django.urls import reverse_lazy
from .models import Grade, Wallet, Book, Purchase,CustomUser
from .forms import GradeForm, WalletForm, BookForm, PurchaseForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Sum
from django.views.generic import DetailView
from django.db.models import Sum
from django.views.generic import DetailView
from django.db.models import Sum
from .models import CustomUser, Purchase
from django.views.generic import DetailView
from django.db.models import Sum, F, Q
from .models import CustomUser, Purchase, Payment
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Payment, Purchase
from .forms import PaymentForm
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Purchase, CustomUser
from django.shortcuts import render
from django.db import models
from django.db.models import Sum
from django.db.models import Sum
from django.views.generic import ListView
from .models import Book
from django.db.models import F
from django.views.generic import ListView
from django.db.models import Q
from .models import Wallet
from django.views.generic import DetailView
from .models import CustomUser, Purchase
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Purchase, Book
from django.db.models import Q
from django.views.generic import DetailView
from .models import Book, Purchase, CustomUser
from django.urls import reverse_lazy
from django.db.models import F

# User logout
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/log_out.html')




# Base and Home pages
class Base(TemplateView):
    template_name = "base.html"

class Home(TemplateView):
    template_name = "home.html"
    
# CRUD for Grade
class GradeListView(ListView):
    model = Grade
    template_name = 'genre_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        queryset = Grade.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset


class GradeDetailView(DetailView):
    model = Grade
    template_name = 'genre_detail.html'
    context_object_name = 'grade'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grade = self.get_object()  # Get the current Grade object

        # Filter students who belong to this grade
        students = CustomUser.objects.filter(grade=grade)

        # Now, filter Wallet objects for each student using a relationship with CustomUser
        wallets = Wallet.objects.filter(student__in=students)  # Filter Wallets related to the students

        context['wallets'] = wallets  # Add the Wallets to the context
        context['students'] = students  # Add the students to the context
        context['total_students'] = students.count()  # Add the total number of students

        return context




class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'genre_form.html'
    success_url = reverse_lazy('grade-list')

    def test_func(self):
        # Only allow staff members to create grades
        return self.request.user.is_staff


class GradeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'genre_form.html'
    success_url = reverse_lazy('grade-list')

    def test_func(self):
        # Only allow staff members to update grades
        return self.request.user.is_staff


        return Response(response.json(), status=status.HTTP_200_OK)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

class LoginPage(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(
            request,
            "registration/login.html",
            {
                "form": form,
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # Ба саҳифаи хона пайваст кунед
        return render(
            request,
            "registration/login.html",
            {
                "form": form,
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )


class GradeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Grade
    template_name = 'genre_confirm_delete.html'
    success_url = reverse_lazy('grade-list')

    def test_func(self):
        # Only allow staff members to delete grades
        return self.request.user.is_staff



class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the total value of books in stock (price * stock)
        total_value = self.get_queryset().aggregate(
            total_value=Sum(F('price') * F('stock'))
        )['total_value'] or 0.00

        # Calculate the total stock quantity (sum of all stock values)
        total_stock = self.get_queryset().aggregate(
            total_stock=Sum('stock')
        )['total_stock'] or 0

        # Add the total value and total stock to the context
        context['total_value'] = total_value
        context['total_stock'] = total_stock

        return context



    

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total sum of all purchases for this book
        total_sum = Purchase.objects.filter(book=self.object, is_paid=True).aggregate(total_sum=Sum('price_paid'))['total_sum'] or 0.00

        # All users (students) who have purchased this book and the quantity each has bought
        users_with_quantity = CustomUser.objects.filter(purchases__book=self.object).distinct()
        user_purchase_data = []

        for user in users_with_quantity:
            total_quantity = Purchase.objects.filter(student=user, book=self.object, is_paid=True).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            user_purchase_data.append({
                'user': user,
                'quantity': total_quantity
            })

        # Stock of the book (assuming there's a field `stock` in your Book model)
        stock = self.object.stock

        # Add the necessary context variables
        context['total_sum'] = total_sum
        context['users'] = user_purchase_data
        context['stock'] = stock

        return context









class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Only allow staff members to create books
        return self.request.user.is_staff


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Only allow staff members to update books
        return self.request.user.is_staff


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Only allow staff members to delete books
        return self.request.user.is_staff


# CRUD for Purchase
class PurchaseListView(ListView):
    model = Purchase
    template_name = 'review_list.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        queryset = Purchase.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(book__title__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(review__icontains=search_query)
            )
        return queryset




class PurchaseDetailView(DetailView):
    model = CustomUser
    template_name = 'c_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Харидҳое, ки пардохт пурра анҷом нашудааст
        unpaid_purchases = (
            Purchase.objects.filter(student=user)
            .annotate(
                total_paid=Sum('payments__amount_paid')  # Маблағи умумии пардохтҳо
            )
            .filter(
                Q(total_paid__lt=F('price_paid')) | Q(total_paid__isnull=True)
            )
        )

        purchases_with_remaining = []
        for purchase in unpaid_purchases:
            remaining_amount = purchase.price_paid - (purchase.total_paid or 0)
            purchases_with_remaining.append({
                'purchase': purchase,
                'remaining_amount': remaining_amount,
            })


        total_unpaid = sum(item['remaining_amount'] for item in purchases_with_remaining)
        context.update({
            'unpaid_purchases': purchases_with_remaining,
            'total_unpaid': total_unpaid,
        })
        return context


    




    

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('purchase-list')

    def form_valid(self, form):
        form.instance.student = self.request.user  # Automatically set the student to the logged-in user
        form.instance.make_purchase()  # Call any additional logic related to making a purchase
        return super().form_valid(form)


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('purchase-list')


class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('purchase-list')


# CRUD for Wallet


class WalletListView(ListView):
    model = Wallet
    template_name = 'borrow_list.html'
    context_object_name = 'wallets'

    def get_queryset(self):
        # Filter the queryset to show only the current user's wallets
        queryset = Wallet.objects.filter(student=self.request.user)
        
        # Optional: Add search functionality (if needed)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(student__username__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset

    


class CustomerDetailView(DetailView):
    model = CustomUser
    template_name = 'c_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current user object
        user = self.get_object()

        # Filter unpaid purchases of this user
        unpaid_purchases = Purchase.objects.filter(student=user, is_paid=False)

        # Prepare a list of unpaid books and calculate the total unpaid price
        unpaid_books = []
        total_unpaid_price = 0

        for purchase in unpaid_purchases:
            unpaid_books.append({
                "title": purchase.book.title,        # Book title
                "quantity": purchase.quantity,      # Quantity purchased
                "price_per_item": purchase.book.price,  # Price per item
                "total_price": purchase.price_paid  # Total price (for the given purchase)
            })
            total_unpaid_price += purchase.price_paid

        # Add unpaid books and total unpaid price to context
        context["unpaid_books"] = unpaid_books
        context["total_unpaid_price"] = total_unpaid_price

        # Retrieve the books purchased by this user (avoid error here)
        purchased_books = []
        for purchase in Purchase.objects.filter(student=user, is_paid=True):
            book = purchase.book  # Ensure this is a Book instance, not just a string
            purchased_books.append({
                'book': book,  # Actual Book instance
                'quantity': purchase.quantity,
                'price_paid': purchase.price_paid
            })

        # Add purchased books to the context
        context["purchased_books"] = purchased_books

        return context







class WalletDetailView(DetailView):
    model = Wallet
    template_name = 'borrow_detail.html'
    context_object_name = 'wallet'
    
    

    def get_object(self):
        # Get the wallet object only if the user has made a purchase
        wallet = get_object_or_404(Wallet, pk=self.kwargs['pk'], user=self.request.user)
        if not self.request.user.purchase_set.exists():
            raise PermissionDenied("You must make a purchase to view your wallet.")
        return wallet



class WalletUpdateView(LoginRequiredMixin, UpdateView):
    model = Wallet
    form_class = WalletForm
    template_name = 'borrow_form.html'
    success_url = reverse_lazy('wallet-list')
    

# CRUD for Payment
class PaymentListView(ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        queryset = Payment.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(student__username__icontains=search_query) |
                Q(purchase__book__title__icontains=search_query) |
                Q(payment_method__icontains=search_query)
            )
        return queryset

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment-list')

    def form_valid(self, form):
        form.instance.student = self.request.user  
        if form.instance.status == 'completed':
            pass
        return super().form_valid(form)