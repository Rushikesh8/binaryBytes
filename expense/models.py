from django.db import models
from accounts.models import CustomUser

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)

class Expense(BaseModel):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SharedExpense(BaseModel):
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(CustomUser, related_name='paid_by', on_delete=models.CASCADE)
    shared_with_users = models.ManyToManyField(CustomUser, related_name='shared_with_users')

    @property
    def individual_amount(self):
        total_amount = self.expense.amount
        num_users = 1 + self.shared_with_users.count()
        individual_amount = total_amount / num_users

        return individual_amount
    
    def mark_user_consent(self, user):
        if user in self.shared_with_users.all() or user == self.paid_by:
            user_consent = SharedExpenseConsent.objects.get_or_create(expense=self, user=user)
            user_consent.consent_received = True
            user_consent.save()
        else:
            raise ValueError("User is not associated with this expense.")
    
class SharedExpenseConsent(models.Model):
    expense = models.ForeignKey(SharedExpense, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    consent_received = models.BooleanField(default=False)

