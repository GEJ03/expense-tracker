import argparse
import sys

from storage import load_data, save_data
from expenses import add_expense, delete_expense, list_expenses, get_summary


def parse_amount(value):
    try:
        amount = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid number")
    if amount <= 0:
        raise argparse.ArgumentTypeError("Amount must be positive")
    return round(amount, 2)


def cmd_add(args):
    data = load_data()
    expense = add_expense(data, args.description, args.amount, args.category)
    save_data(data)
    print(f"Added expense #{expense['id']}: {expense['description']} ${expense['amount']:.2f}")


def cmd_list(args):
    data = load_data()
    expenses = list_expenses(data, category=args.category)
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':>8}  Description")
    print("-" * 55)
    for e in expenses:
        cat = e["category"] or "-"
        print(f"{e['id']:<5} {e['date']:<12} {cat:<15} ${e['amount']:>7.2f}  {e['description']}")


def cmd_delete(args):
    data = load_data()
    try:
        delete_expense(data, args.id)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    save_data(data)
    print(f"Deleted expense #{args.id}")


def cmd_summary(args):
    data = load_data()
    total = get_summary(data, month=args.month)
    label = f" for {args.month}" if args.month else ""
    print(f"Total expenses{label}: ${total:.2f}")


def main():
    parser = argparse.ArgumentParser(prog="expense_tracker", description="CLI Expense Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new expense")
    p_add.add_argument("description", help="Short description of the expense")
    p_add.add_argument("amount", type=parse_amount, help="Amount (positive number)")
    p_add.add_argument("--category", default=None, help="Optional category label")

    p_list = sub.add_parser("list", help="List expenses")
    p_list.add_argument("--category", default=None, help="Filter by category")

    p_del = sub.add_parser("delete", help="Delete an expense by ID")
    p_del.add_argument("id", type=int, help="Expense ID to delete")

    p_sum = sub.add_parser("summary", help="Show total spending")
    p_sum.add_argument("--month", default=None, metavar="YYYY-MM", help="Filter by month")

    args = parser.parse_args()
    {"add": cmd_add, "list": cmd_list, "delete": cmd_delete, "summary": cmd_summary}[args.command](args)


if __name__ == "__main__":
    main()
