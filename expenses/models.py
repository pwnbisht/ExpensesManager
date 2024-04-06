from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    mobile = models.CharField(max_length=10, null=True, blank=True)
    balances = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def owed_amount_to_payer(self, payer, amount):
        payer_id = str(payer.id)
        if payer_id in self.balances:
            self.balances[payer_id] += amount
        else:
            self.balances[payer_id] = amount
        self.save()

    def get_balances(self):
        balances = []
        for user_id, amount in self.balances.items():
            user = User.objects.get(id=int(user_id))
            balance = {
                'user': user.name,
                'amount': amount
            }
            balances.append(balance)
        return balances


class Expense(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    amount = models.FloatField(validators=[MaxValueValidator(10000000)], max_length=8)
    type_choices = (
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENT', 'Percent'),
    )
    expense_type = models.CharField(max_length=10, choices=type_choices, default='EQUAL')
    participants = models.ManyToManyField(User, related_name='expenses_involved')

    def __str__(self):
        return f"{self.payer} - {self.amount}"
