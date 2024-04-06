import csv
from io import StringIO
from celery import shared_task
from django.conf import settings
from .models import User, Expense
import boto3


@shared_task
def export_data_to_s3():
    # Fetch data from the User and Expense models
    users = User.objects.all()
    expenses = Expense.objects.all()

    # Generate CSV data for users
    user_csv_data = StringIO()
    user_csv_writer = csv.writer(user_csv_data)
    user_csv_writer.writerow(['Name', 'Email', 'Mobile'])
    for user in users:
        user_csv_writer.writerow([user.name, user.email, user.mobile])

    # Generate CSV data for expenses
    expense_csv_data = StringIO()
    expense_csv_writer = csv.writer(expense_csv_data)
    expense_csv_writer.writerow(['Payer', 'Amount', 'Expense Type'])
    for expense in expenses:
        expense_csv_writer.writerow([expense.payer.name, expense.amount, expense.expense_type])

    # Upload the CSV files to Amazon S3
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = 'bucket-name'

    # Upload user data
    user_file_name = 'users.csv'
    s3.put_object(Bucket=bucket_name, Key=user_file_name, Body=user_csv_data.getvalue())

    # Upload expense data
    expense_file_name = 'expenses.csv'
    s3.put_object(Bucket=bucket_name, Key=expense_file_name, Body=expense_csv_data.getvalue())
