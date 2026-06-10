import csv

import os

from datetime import datetime

class MainModel:

    def __init__(self):

        self.file_path = "data/transactions.csv"

        self.fieldnames = ["id", "type", "date", "description", "amount", "category"]

        if not os.path.exists("data"):

            os.makedirs("data")

        if not os.path.exists(self.file_path):

            self.create_csv_file()

        else:

            self.upgrade_csv_file()

    def create_csv_file(self):

        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            writer.writeheader()

    def upgrade_csv_file(self):

        with open(self.file_path, mode="r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            old_fieldnames = reader.fieldnames

            rows = list(reader)

        if old_fieldnames is None:

            self.create_csv_file()

            return

        if old_fieldnames == self.fieldnames:

            return

        new_rows = []

        for row in rows:

            new_rows.append({

                "id": row.get("id", ""),

                "type": row.get("type", ""),

                "date": row.get("date", ""),

                "description": row.get("description", ""),

                "amount": row.get("amount", "0"),

                "category": row.get("category", "Khác") or "Khác"

            })

        self.save_all_transactions(new_rows)

    def get_all_transactions(self):

        transactions = []

        if not os.path.exists(self.file_path):

            self.create_csv_file()

        with open(self.file_path, mode="r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if "category" not in row or row["category"] == "":

                    row["category"] = "Khác"

                transactions.append(row)

        return transactions

    def create_new_id(self):

        transactions = self.get_all_transactions()

        if len(transactions) == 0:

            return 1

        ids = [int(transaction["id"]) for transaction in transactions if str(transaction.get("id", "")).isdigit()]

        if len(ids) == 0:

            return 1

        return max(ids) + 1

    def add_transaction(self, transaction_type, date, description, amount, category):

        new_id = self.create_new_id()

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([new_id, transaction_type, date, description, amount, category])

    def update_transaction(self, transaction_id, transaction_type, date, description, amount, category):

        transactions = self.get_all_transactions()

        for transaction in transactions:

            if transaction["id"] == str(transaction_id):

                transaction["type"] = transaction_type

                transaction["date"] = date

                transaction["description"] = description

                transaction["amount"] = amount

                transaction["category"] = category

                break

        self.save_all_transactions(transactions)

    def delete_transaction(self, transaction_id):

        transactions = self.get_all_transactions()

        new_transactions = [transaction for transaction in transactions if transaction["id"] != str(transaction_id)]

        self.save_all_transactions(new_transactions)

    def save_all_transactions(self, transactions):

        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            writer.writeheader()

            for transaction in transactions:

                writer.writerow({

                    "id": transaction.get("id", ""),

                    "type": transaction.get("type", ""),

                    "date": transaction.get("date", ""),

                    "description": transaction.get("description", ""),

                    "amount": transaction.get("amount", "0"),

                    "category": transaction.get("category", "Khác") or "Khác"

                })

    def normalize_transaction_row(self, row, new_id=None):

        transaction_id = row.get("id") or row.get("ID") or row.get("Mã") or row.get("Ma") or ""

        transaction_type = row.get("type") or row.get("Loại") or row.get("Loai") or row.get("Loại giao dịch") or row.get("Loai giao dich") or ""

        date = row.get("date") or row.get("Ngày") or row.get("Ngay") or ""

        description = row.get("description") or row.get("Nội dung") or row.get("Noi dung") or row.get("Mô tả") or row.get("Mo ta") or ""

        amount = row.get("amount") or row.get("Số tiền") or row.get("So tien") or "0"

        category = row.get("category") or row.get("Danh mục") or row.get("Danh muc") or "Khác"

        if new_id is not None:

            transaction_id = str(new_id)

        transaction_type = str(transaction_type).strip()

        if transaction_type.lower() in ["thu", "thu nhap", "thu nhập", "income"]:

            transaction_type = "Thu nhập"

        elif transaction_type.lower() in ["chi", "chi tieu", "chi tiêu", "expense"]:

            transaction_type = "Chi tiêu"

        return {

            "id": str(transaction_id).strip(),

            "type": transaction_type,

            "date": str(date).strip(),

            "description": str(description).strip(),

            "amount": str(amount).replace(",", "").strip(),

            "category": str(category).strip() or "Khác"

        }

    def import_csv_file(self, import_file_path, replace_data=False):

        with open(import_file_path, mode="r", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            rows = list(reader)

        if reader.fieldnames is None:

            raise ValueError("File CSV không có dòng tiêu đề.")

        current_transactions = [] if replace_data else self.get_all_transactions()

        ids = [int(t.get("id", 0)) for t in current_transactions if str(t.get("id", "")).isdigit()]

        next_id = max(ids) + 1 if ids else 1

        imported_count = 0

        for row in rows:

            if not any(str(value).strip() for value in row.values() if value is not None):

                continue

            transaction = self.normalize_transaction_row(row, new_id=next_id)

            if transaction["type"] not in ["Thu nhập", "Chi tiêu"]:

                continue

            if transaction["date"] == "" or transaction["description"] == "":

                continue

            if self.to_float(transaction["amount"]) <= 0:

                continue

            current_transactions.append(transaction)

            imported_count += 1

            next_id += 1

        self.save_all_transactions(current_transactions)

        return imported_count

    def export_csv_file(self, export_file_path, transactions=None):

        if transactions is None:

            transactions = self.get_all_transactions()

        with open(export_file_path, mode="w", newline="", encoding="utf-8-sig") as file:

            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            writer.writeheader()

            for transaction in transactions:

                writer.writerow({

                    "id": transaction.get("id", ""),

                    "type": transaction.get("type", ""),

                    "date": transaction.get("date", ""),

                    "description": transaction.get("description", ""),

                    "amount": transaction.get("amount", "0"),

                    "category": transaction.get("category", "Khác") or "Khác"

                })

        return export_file_path

    def to_float(self, value):

        try:

            return float(str(value).replace(",", "").strip())

        except ValueError:

            return 0

    def parse_date(self, date_text):

        try:

            return datetime.strptime(date_text, "%d/%m/%Y")

        except ValueError:

            return None

    def get_total_income(self):

        transactions = self.get_all_transactions()

        return sum(self.to_float(t["amount"]) for t in transactions if t["type"] == "Thu nhập")

    def get_total_expense(self):

        transactions = self.get_all_transactions()

        return sum(self.to_float(t["amount"]) for t in transactions if t["type"] == "Chi tiêu")

    def get_balance(self):

        return self.get_total_income() - self.get_total_expense()

    def search_transactions(

        self,

        keyword="",

        transaction_type="Tất cả",

        category="Tất cả",

        date_from=None,

        date_to=None,

        min_amount=None,

        max_amount=None

    ):

        transactions = self.get_all_transactions()

        keyword = keyword.lower().strip()

        date_from_dt = self.parse_date(date_from) if date_from else None

        date_to_dt = self.parse_date(date_to) if date_to else None

        min_amount_val = self.to_float(min_amount) if min_amount not in (None, "") else None

        max_amount_val = self.to_float(max_amount) if max_amount not in (None, "") else None

        results = []

        for transaction in transactions:

            current_type = transaction.get("type", "")

            current_category = transaction.get("category", "Khác")

            current_date = self.parse_date(transaction.get("date", ""))

            current_amount = self.to_float(transaction.get("amount", "0"))

            if transaction_type != "Tất cả" and current_type != transaction_type:

                continue

            if category != "Tất cả" and current_category != category:

                continue

            if date_from_dt and (current_date is None or current_date < date_from_dt):

                continue

            if date_to_dt and (current_date is None or current_date > date_to_dt):

                continue

            if min_amount_val is not None and current_amount < min_amount_val:

                continue

            if max_amount_val is not None and current_amount > max_amount_val:

                continue

            searchable_text = " ".join([

                str(transaction.get("id", "")),

                str(transaction.get("type", "")),

                str(transaction.get("date", "")),

                str(transaction.get("description", "")),

                str(transaction.get("amount", "")),

                str(transaction.get("category", "Khác"))

            ]).lower()

            if keyword == "" or keyword in searchable_text:

                results.append(transaction)

        return results

    def get_expenses_by_category(self, transactions=None):

        if transactions is None:

            transactions = self.get_all_transactions()

        expenses = {}

        for transaction in transactions:

            if transaction.get("type") == "Chi tiêu":

                category = transaction.get("category", "Khác") or "Khác"

                amount = self.to_float(transaction.get("amount", "0"))

                expenses[category] = expenses.get(category, 0) + amount

        return expenses

    def get_expense_percentage_by_category(self, transactions=None):

        expenses = self.get_expenses_by_category(transactions)

        total_expense = sum(expenses.values())

        if total_expense == 0:

            return {category: (amount, 0.0) for category, amount in expenses.items()}

        return {

            category: (amount, round(amount / total_expense * 100, 2))

            for category, amount in expenses.items()

        }

    def get_expenses_by_month(self, transactions=None):

        if transactions is None:

            transactions = self.get_all_transactions()

        monthly_expenses = {}

        for transaction in transactions:

            if transaction.get("type") != "Chi tiêu":

                continue

            date_value = self.parse_date(transaction.get("date", ""))

            if date_value is None:

                continue

            month_key = date_value.strftime("%m/%Y")

            amount = self.to_float(transaction.get("amount", "0"))

            monthly_expenses[month_key] = monthly_expenses.get(month_key, 0) + amount

        return monthly_expenses
