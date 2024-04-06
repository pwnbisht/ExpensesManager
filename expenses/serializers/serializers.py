from rest_framework import serializers
from expenses.models import User, Expense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'mobile']


class BalanceSerializer(serializers.Serializer):
    user = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ExpenseSerializer(serializers.ModelSerializer):
    payer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    amount = serializers.FloatField()

    class Meta:
        model = Expense
        fields = ['payer', 'amount', 'expense_type', 'participants']

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        expense = Expense.objects.create(**validated_data)
        expense.participants.set(participants)
        return expense
