from django.urls import path
from .views import *

urlpatterns = [
    path('Home', Base.as_view(), name='base'),
    path('', Home.as_view(), name='home'),
    path('logout/', user_logout, name='logout'),
    path('login/', LoginPage.as_view(), name='login/ssh'),


    # URL-ҳои Grade
    path('grades/', GradeListView.as_view(), name='grade-list'),
    path('grades/create/', GradeCreateView.as_view(), name='grade-create'),
    path('grades/<int:pk>/update/', GradeUpdateView.as_view(), name='grade-update'),
    path('grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade-delete'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),  # Detail View

    # URL-ҳои Book
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Detail View

    # URL-ҳои Purchase
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('purchases/create/', PurchaseCreateView.as_view(), name='purchase-create'),
    path('purchases/<int:pk>/update/', PurchaseUpdateView.as_view(), name='purchase-update'),
    path('purchases/<int:pk>/delete/', PurchaseDeleteView.as_view(), name='purchase-delete'),
    path('purchases/<int:pk>/', PurchaseDetailView.as_view(), name='purchase-detail'),  # Detail View

    # URL-ҳои Wallet
    path('wallets/', WalletListView.as_view(), name='wallet-list'),
    path('wallets/<int:pk>/update/', WalletUpdateView.as_view(), name='wallet-update'),
    path('customer/<int:pk>/', PurchaseDetailView.as_view(), name='cdetail'),  # Detail View
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/new/', PaymentCreateView.as_view(), name='payment-create'),

]