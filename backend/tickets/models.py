from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    STATUS_CHOICES =[
        ('open','Open'),
        ('in_progress','In Progress'),
        ('closed','Closed'),
    ]

    PRIORITY_CHOICES=[
        ('low', 'Low'),
        ('medium','Medium'),
        ('high','High'),
    ]
    # CATEGORY_CHOICES=[
    #     ('BILLING','Billing'),
    #     ('TECHNICAL','Technaical'),
    #     ('ACCOUNTS','Accounts'),
    #     ('OTHERS','Others'),
    # ]

    title=models.CharField(max_length=255)
    description=models.TextField()
    
    #who created the ticket
    customer=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tickets',
        
    )

    #Assigned support agent 
    assigned_to =models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    # category =models.CharField(max_length=20,choices=CATEGORY_CHOICES,default="OTHERS")
    category= models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="tickets")

    sentiment_score = models.FloatField(null=True,blank=True)

    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='open')

    priority=models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='low')

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at =models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"