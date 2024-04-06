from typing import Optional, Dict, Any

from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from .models import User, Expense
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers.serializers import UserSerializer, ExpenseSerializer, BalanceSerializer


# User views
@api_view(['GET'])
def user_list(request: Request) -> Response:
    """
       Get a list of all users.

       Args:
       - request (Request): The request object.

       Returns:
       - Response: A response containing the serialized user data.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_detail(request: Request, pk: int) -> Response:
    """
        Get details of a specific user.

        Args:
        - request (Request): The request object.
        - pk (int): The primary key of the user.

        Returns:
        - Response: A response containing the serialized user data.
    """
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def user_create(request: Request) -> Response:
    """
        Create a new user.

        Parameters:
        request (Request): The request object containing user data.

        Returns:
        Response: The response object with the created user data or errors.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Expense views
@api_view(['GET'])
def expense_list(request: Request) -> Response:
    """
    Retrieve a list of all expenses.

    Parameters:
    request (Request): The request object.

    Returns:
    Response: A response containing the serialized list of expenses.
    """
    expenses = Expense.objects.all()
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def expense_detail(request: Request, pk: int) -> Response:
    """
    Retrieve a list of all expenses.
    Args:
        - request (Request): The request object.
        - pk (int): The primary key of the user.
    Returns:
        - Response: A response containing the serialized list of expenses.
    """
    user = get_object_or_404(User, pk=pk)
    balances = user.get_balances()
    serializer = BalanceSerializer(balances, many=True)
    return Response(serializer.data)


def split_expense(expense: Expense, split_type: str, exact_amounts: Optional[Dict[int, float]] = None,
                  percentages: Optional[Dict[Any, float]] = None) -> None:
    """
    Split the expense among participants based on the split type.

    Parameters:
    expense (Expense): The expense object to split.
    split_type (str): The type of split to be performed.
    exact_amounts (Optional[Dict[int, float]]): A dictionary with participant ID as key and exact amount as value.
    percentages (Optional[Dict[int, float]]): A dictionary with participant ID as key and percentage as value.
    """
    participants = list(expense.participants.all())
    num_participants = len(participants)

    if num_participants == 0:
        return

    if split_type == 'EQUAL':
        split_amount = expense.amount / num_participants
        for participant in participants:
            if participant != expense.payer:
                participant.owed_amount_to_payer(expense.payer, split_amount)
    elif split_type == 'EXACT':
        for participant, amount in exact_amounts.items():
            participant_obj = User.objects.get(id=participant)
            if participant_obj != expense.payer:
                participant_obj.owed_amount_to_payer(expense.payer, amount)
    elif split_type == 'PERCENT':
        for participant, percentage in percentages.items():
            amount_to_pay = (expense.amount * percentage) / 100
            participant_obj = User.objects.get(id=participant)
            if participant_obj != expense.payer:
                participant_obj.owed_amount_to_payer(expense.payer, amount_to_pay)


@api_view(['POST'])
def expense_create(request: Request) -> Response:
    """
    Create an expense.

    Parameters:
        request (Request): The request object containing expense data.

    Returns:
        Response: The response object with the created expense data or errors.
    """
    serializer = ExpenseSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            expense = serializer.save()
            expense.full_clean()
            split_type = serializer.validated_data.get('expense_type')
            if split_type == 'EXACT':
                exact_amounts = request.data.get('exact_amounts', {})
                total_exact_amount = sum(exact_amounts.values())

                if total_exact_amount != expense.amount:
                    return Response({"error": "Total exact amounts must be equal to the total expense amount."},
                                    status=status.HTTP_400_BAD_REQUEST)

                participants_in_expense = set(expense.participants.values_list('id', flat=True))
                participants_in_request = set(map(int, exact_amounts.keys()))
                invalid_participants = participants_in_request - participants_in_expense
                if invalid_participants:
                    return Response(
                        {
                            "error": f"The following participants are not part of the expense: {', '.join(map(str, invalid_participants))}."},
                        status=status.HTTP_400_BAD_REQUEST)

                split_expense(expense, split_type, exact_amounts)
            elif split_type == 'PERCENT':
                percentages = request.data.get('percentages', {})
                total_percentage = sum(percentages.values())

                if total_percentage != 100:
                    return Response({"error": "Total percentage shares must sum up to 100."},
                                    status=status.HTTP_400_BAD_REQUEST)

                participants_in_expense = set(expense.participants.values_list('id', flat=True))
                participants_in_request = set(map(int, percentages.keys()))
                invalid_participants = participants_in_request - participants_in_expense
                if invalid_participants:
                    return Response(
                        {
                            "error": f"The following participants are not part of the expense: {', '.join(map(str, invalid_participants))}."},
                        status=status.HTTP_400_BAD_REQUEST)

                split_expense(expense, split_type, percentages=percentages)
            else:
                split_expense(expense, split_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_dict = {'error': str(e)}
        return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)
