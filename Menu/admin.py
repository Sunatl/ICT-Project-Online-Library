from django.contrib import admin
from .models import Grade, CustomUser, Wallet, Book, Purchase, Payment

# Танзими Grade дар админ
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Намоиш дар рӯйхат
    search_fields = ('name',)  # Ҷустуҷӯ бо номи синф

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'grade', 'phone_number')  # Намоиш дар рӯйхат
    search_fields = ('username', 'email',)  # Ҷустуҷӯ
    list_filter = ('grade',)  # Филтр бо синф

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('student', 'balance')  # Намоиш дар рӯйхат
    search_fields = ('student__username', 'student__email')  # Ҷустуҷӯ бо номи талабагӣ

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'is_available')  # Намоиш дар рӯйхат
    search_fields = ('title',)  # Ҷустуҷӯ бо номи китоб
    list_filter = ('is_available',)  # Филтр бо дастрасӣ

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'purchase_date', 'quantity', 'price_paid', 'is_paid')  # Намоиш дар рӯйхат
    search_fields = ('student__username', 'book__title')  # Ҷустуҷӯ бо номи талабагӣ ва китоб
    list_filter = ('is_paid', 'purchase_date')  # Филтр бо ҳолати пардохт ва таърих


admin.site.register(Payment)
