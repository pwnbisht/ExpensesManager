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
- `**GET users/**`: Get List of Users or available participants
