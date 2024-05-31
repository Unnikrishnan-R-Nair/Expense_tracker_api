from django.db import models

from django.contrib.auth.models import User


class Expense(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    category_choices = (
        ("Food", "Food"),
        ("Transportation", "Transportation"),
        ("House_Rent", "House_Rent"),
        ("Water_Bill", "Water_Bill"),
        ("Electricity_Bill", "Electricity_Bill"),
        ("Hospital_Bill", "Hospital_Bill"),
        ("Education", "Education"),
        ("Personal_Care", "Personal_Care"),
        ("Debt_Payment", "Dept_Payment"),
        ("EMI", "EMI"),
        ("Entertainment", "Entertainment"),
        ("Recharges", "Recharges"),
        ("Savings", "Savings"),
        ("Miscellaneous", "Miscellaneous")
    )

    category = models.CharField(max_length=100, choices=category_choices, default="Miscellaneous")

    amount = models.PositiveIntegerField()

    priority_choices = (
        ("need", "need"),
        ("want", "want"),
    )

    priority = models.CharField(max_length=50, choices=priority_choices, default="need")

    created_date = models.DateField(auto_now_add=True)

    def __str__(self):

        return self.title



class Income(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    category_options = (
        ("Salary", "Salary"),
        ("Interest", "Interest"),
        ("Business", "Business"),
        ("Rental", "Rental"),
        ("Agriculture", "Agriculture"),
        ("Freelancing", "Freelancing"),
        ("Stock_Trading", "Stock_Trading"),
        ("Dividend", "Dividend"),
        ("Royalty", "Royalty"),
        ("Capital", "Capital"),
        ("Pension", "Pension"),
        ("SocialSecurity", "SocialSecurity"),
        ("Other", "Other"),
    )

    category = models.CharField(max_length=100, choices=category_options, default="Salary")

    amount = models.PositiveIntegerField()

    created_date = models.DateField(auto_now_add=True)

    def __str__(self):

        return self.title