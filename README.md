# Expense Management

Welcome to the Django API project! This repository contains the source code for our backend(Django/DRF).

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
  
## About
Expense Manager is a Django REST API application that helps users manage their expenses among a group of friends or collaborators. The application allows users to create expenses, split them among participants, and track balances.

## Features
- **Expense Creation:** Users can create expenses with details such as the payer, amount, expense type, and participants.
- **Expense Splitting:** Expenses can be split equally, based on exact amounts, or percentage shares among participants.
- **Validation:** The application validates expense amounts and split details to ensure accuracy.
- **Balances:** Users can view their balances with other participants, showing who owes whom and how much.

## Getting Started

### Prerequisites

List any prerequisites or dependencies that users need to install to get your project up and running. For example:
- [Python](https://www.python.org/downloads/) (3.12)

### Installation

### Step 1: Clone the Repository

You can get the source code by cloning this repository to your local machine. Open your terminal and run the following command:
```bash
git clone https://github.com/pwnbisht/ExpensesManager.git
```
### Step 2: Change your working directory to the newly cloned repository:
```bash
cd ExpensesManager
```
### Step 3: Install dependencies:
```bash
pip install -r requirements.txt
```
### Step 4: Make migrations:
```bash
python manage.py makemigrations
```
### Step 5: Apply Migrations:
```bash
python manage.py migrate
```
### Step 6: Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The Expense Manager API provides the following endpoints:
- **`GET users/`** : Get List of Users or available participants
- **`GET users/<user_id>/`** : Get Details of an indivisual User
- **`POST users/create/`** : Create Users
  - request body:
    ```bash
    {
      "name": "Pawan Bisht",
      "email": "xyz@xyz.com",
      "mobile": "1231231231"
    }
    ```
- **`GET /expenses/`** : Get list of expenses
- **`GET /expenses/<user_id>/`** : get the expenses details of User
  - Response:
      ```bash
      [
          {
              "user": "User2",    // user_id(User3) owes User2: 115.00
              "amount": "115.00"
          }
      ]
      ```
- **`POST expenses/create/`**: Split the expenses
  - request body if expense type is EQUAL:
      ```bash
      {
          "payer": <user_id>,      // who is paying
          "amount": 100,           // total amount
          "expense_type": "EQUAL",
          "participants": [<user_id1>, <user_id2>, <user_id3>]    // list of participants
      }
    ```
      
  - if expense type is EXACT:
      ```bash
      {
          "payer": <user_id>,
          "amount": 100,
          "expense_type": "EXACT",
          "participants": [<user_id1>, <user_id2>, <user_id3>],
          "exact_amounts": {
              "<user_id1>": 40,
              "<user_id2>": 30,
              "<user_id3>": 30
          }
      }
      ```
  - if expsnse type is PERCENT
      ```bash
      {
          "payer": <user_id>,
          "amount": 100,
          "expense_type": "PERCENT",
          "participants": [<user_id>,<user_id>],
          "percentages": {
              "<user_id>": 40,
              "<user_id>": 60
          }
      }
      ```
Example: This month's electricity bill was Rs. 1000.
  Now you can just go to the app and add that you paid 1000, select all the 4
  people and then select split equally.
  Input: u1 paid Rs 1000/- for u1 u2 u3 u4 and needs to be split EQUALLY
  For this transaction, everyone owes Rs 250 to User1. The app should
  update the balances in each of the profiles accordingly.
  User2 owes User1: Rs 250
  User3 owes User1: Rs 250
  User4 owes User1: Rs 250

  Let user_id of User1, User2, User3, User4 are respectively 1,2,3,4 then:

  Request Body:
  ```bash
  {
      "payer": 1,
      "amount": 1000,
      "expense_type": "EQUAL",
      "participants": [1,2,3,4]    // list of participants
  }
```
