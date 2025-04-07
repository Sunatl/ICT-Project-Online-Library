from django.contrib import admin
from .models import Grade, CustomUser, Wallet, Book, Purchase, Payment, StudentBook, School, Category

# Танзими Grade дар админ
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Намоиш дар рӯйхат
    search_fields = ('name',)  # Ҷустуҷӯ бо номи синф

# Танзими CustomUser дар админ
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'grade', 'phone_number')  # Намоиш дар рӯйхат
    search_fields = ('username', 'email',)  # Ҷустуҷӯ
    list_filter = ('grade','school')  # Филтр бо синф

# Танзими Wallet дар админ
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('student', 'balance')  # Намоиш дар рӯйхат
    search_fields = ('student__username', 'student__email')  # Ҷустуҷӯ бо номи талабагӣ

# Танзими Book дар админ
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'is_available')  # Намоиш дар рӯйхат
    search_fields = ('title',)  # Ҷустуҷӯ бо номи китоб
    list_filter = ('is_available',)  # Филтр бо дастрасӣ

# Танзими Purchase дар админ
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'purchase_date', 'quantity', 'price_paid', 'is_paid')  # Намоиш дар рӯйхат
    search_fields = ('student__username', 'book__title')  # Ҷустуҷӯ бо номи талабагӣ ва китоб
    list_filter = ('is_paid', 'purchase_date')  # Филтр бо ҳолати пардохт ва таърих

# Register School model
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'date')
    search_fields = ('name', 'address')
    list_filter = ('date',)

admin.site.register(School, SchoolAdmin)

# Register StudentBook model
class StudentBookAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'quantity', 'borrowed_at', 'school')
    search_fields = ('student__username', 'book__title', 'school__name')
    list_filter = ('borrowed_at', 'school')

admin.site.register(StudentBook, StudentBookAdmin)

# Register Payment model
admin.site.register(Payment)
