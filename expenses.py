from datetime import date


def add_expense(data, description, amount, category=None):
    expense = {
        "id": data["next_id"],
        "date": date.today().isoformat(),
        "description": description,
        "amount": amount,
        "category": category,
    }
    data["expenses"].append(expense)
    data["next_id"] += 1
    return expense


def delete_expense(data, expense_id):
    for i, e in enumerate(data["expenses"]):
        if e["id"] == expense_id:
            data["expenses"].pop(i)
            return
    raise ValueError(f"No expense found with id {expense_id}")


def list_expenses(data, category=None):
    expenses = data["expenses"]
    if category is not None:
        expenses = [e for e in expenses if e["category"] and e["category"].lower() == category.lower()]
    return expenses


def get_summary(data, month=None):
    expenses = data["expenses"]
    if month is not None:
        expenses = [e for e in expenses if e["date"].startswith(month)]
    return round(sum(e["amount"] for e in expenses), 2)
