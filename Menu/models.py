from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



    
class Category(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
    
class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")  # Алоқаманд бо Grade
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_actives = models.BooleanField(default=False)  
    school = models.ForeignKey("School", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.grade.name if self.grade else 'No Grade'})"


class Wallet(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.student.username} - {self.balance} сомонӣ"

    def add_balance(self, amount):
        if amount < 0:
            raise ValueError("Маблағ бояд мусбӣ бошад!")
        self.balance += amount
        self.save()

    def subtract_balance(self, amount):
        if amount < 0:
            raise ValueError("Маблағ бояд мусбӣ бошад!")
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Маблағи кофӣ дар ҳисоб нест!")

    def has_enough_balance(self, amount):
        return self.balance >= amount

    def get_transaction_history(self):
        return self.transactions.all()

    def reset_balance(self):
        self.balance = 0
        self.save()

@receiver(post_save, sender=CustomUser)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(student=instance, balance=0)


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.PositiveIntegerField(default=0) 
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE ,null=True,blank=True)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)


    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        
    def save(self):
        super().save()
        
    def __str__(self):
        return self.title
    
    

    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.is_available = self.stock > 0
            self.save()
        else:
            raise ValueError("Китоб кофӣ нест дар саҳом!")

    def is_in_stock(self):
        return self.stock > 0
    
    
class School(models.Model):
    name = models.CharField(max_length=255, verbose_name="Номи мактаб")
    address = models.TextField(verbose_name="Нақшаи мактаб")
    phone_number = models.CharField(max_length=15, verbose_name="Рақами телефон")
    date = models.DateField(default=timezone.now, verbose_name="Таърихи таъсисёбӣ")
    books = models.ForeignKey(Book, related_name='schools',null=True, blank=True, verbose_name="Китобҳои мактаб", on_delete=models.CASCADE)
    students_book = models.ForeignKey(CustomUser, related_name='books',null=True, blank=True, verbose_name="Китобҳое, ки аз ҷониби донишҷӯён гирифта шудаанд",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мактаб"
        verbose_name_plural = "Мактабҳо"


# Модели StudentBook (Миёна барои пайваст кардани донишҷӯён ва китобҳо)
class StudentBook(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Донишҷӯ")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Китоб")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Миқдори китоб")
    borrowed_at = models.DateTimeField(auto_now_add=True, verbose_name="Вақти гирифтани китоб")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="Мактаб")  # ForeignKey ба School илова карда шуд

    def __str__(self):
        return f"{self.student.username} - {self.book.title} ({self.quantity} китоб)"

    class Meta:
        verbose_name = "Китоби донишҷӯ"
        verbose_name_plural = "Китобҳои донишҷӯён"




class Purchase(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="purchases")  # Харидор
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)  
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    school = models.ForeignKey("School", on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE,related_name="grade",null=True,blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.book.title} ({'Paid' if self.is_paid else 'Not Paid'})"

    def make_purchase(self): 
        total_price = self.quantity * self.book.price

        if self.book.stock < self.quantity:
            raise ValueError("Китоб кофӣ нест дар саҳом!")
        
        self.book.reduce_stock(self.quantity)

        self.student.wallet.add_balance(total_price)
        self.price_paid = total_price
        self.save()

    def pay(self):
        if self.is_paid:
            raise ValueError("Харид аллакай пардохт шудааст!")
        
        if not self.student.wallet.has_enough_balance(self.price_paid):
            raise ValueError("Маблағи кофӣ дар ҳисоби талабагӣ нест!")
        
        self.student.wallet.subtract_balance(self.price_paid)
        self.is_paid = True
        self.save()

class Payment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")  
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="payments")  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    payment_date = models.DateTimeField(auto_now_add=True)  # Payment date
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('card', 'Card'), ('online', 'Online')])  # Payment method
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending')  

    def __str__(self):
        return f"Payment of {self.amount_paid} by {self.student.username} for {self.purchase.book.title} on {self.payment_date}"
    def save(self, *args, **kwargs):
            wallet = self.student.wallet  # wallet-и донишҷӯ
            if wallet.balance >= self.amount_paid:
                wallet.subtract_balance(self.amount_paid)  # Аз донишҷӯ маблағро мегирем

                # Ба роҳбари синф (ё фурӯшанда) маблағ медиҳем
                class_leader_wallet = self.purchase.class_leader.wallet  
                class_leader_wallet.balance += self.amount_paid
                class_leader_wallet.save()

                self.status = 'completed'
                super().save(*args, **kwargs)
            else:
                raise ValueError("Insufficient funds in the wallet")

def create_payment(purchase):
    if purchase.is_paid:  
        payment = Payment.objects.create(
            student=purchase.student, 
            purchase=purchase, 
            amount_paid=purchase.price_paid, 
            payment_method='card',  
            status='completed'
        )
        return payment
    else:
        raise ValueError("Харид то ҳол пардохт нашудааст!")
