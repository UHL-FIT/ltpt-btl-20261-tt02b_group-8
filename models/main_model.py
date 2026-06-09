# Import thu vien csv de doc va ghi du lieu CSV
import csv

# Import thu vien os de kiem tra thu muc va file
import os

# Import datetime de xu ly ngay thang
from datetime import datetime


# Tao lop MainModel, day la phan Model trong mo hinh MVC
class MainModel:
    # Ham khoi tao, tu chay khi tao doi tuong MainModel
    def __init__(self):
        # Luu duong dan file CSV
        self.file_path = "data/transactions.csv"

        # Khai bao danh sach cot chuan cua file CSV
        self.fieldnames = ["id", "type", "date", "description", "amount", "category"]

        # Neu chua co thu muc data thi tao moi
        if not os.path.exists("data"):
            os.makedirs("data")

        # Neu chua co file CSV thi tao file moi
        if not os.path.exists(self.file_path):
            self.create_csv_file()
        else:
            # Neu file CSV cu chua dung cau truc thi tu nang cap file
            self.upgrade_csv_file()

    # Ham tao file CSV moi
    def create_csv_file(self):
        # Mo file CSV o che do ghi
        with open(self.file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            # Tao doi tuong DictWriter
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            # Ghi dong tieu de
            writer.writeheader()

    # Ham nang cap file CSV cu sang cau truc moi
    def upgrade_csv_file(self):
        # Mo file CSV de doc tieu de hien tai
        with open(self.file_path, mode="r", encoding="utf-8-sig") as file:
            # Doc CSV theo dang dictionary
            reader = csv.DictReader(file)

            # Lay danh sach cot cu
            old_fieldnames = reader.fieldnames

            # Lay toan bo dong du lieu cu
            rows = list(reader)

        # Neu file rong hoac khong co tieu de thi tao lai file moi
        if old_fieldnames is None:
            self.create_csv_file()
            return

        # Neu file da dung cau truc thi khong can lam gi
        if old_fieldnames == self.fieldnames:
            return

        # Tao danh sach du lieu moi theo dung cot chuan
        new_rows = []

        # Duyet tung dong cu
        for row in rows:
            # Them dong moi vao danh sach
            new_rows.append({
                "id": row.get("id", ""),
                "type": row.get("type", ""),
                "date": row.get("date", ""),
                "description": row.get("description", ""),
                "amount": row.get("amount", "0"),
                "category": row.get("category", "Khác") or "Khác"
            })

        # Ghi lai file CSV theo cau truc moi
        self.save_all_transactions(new_rows)

    # Ham lay toan bo giao dich
    def get_all_transactions(self):
        # Tao danh sach rong de chua giao dich
        transactions = []

        # Neu file chua ton tai thi tao moi
        if not os.path.exists(self.file_path):
            self.create_csv_file()

        # Mo file CSV o che do doc
        with open(self.file_path, mode="r", encoding="utf-8-sig") as file:
            # Doc CSV theo dang dictionary
            reader = csv.DictReader(file)

            # Duyet tung dong du lieu
            for row in reader:
                # Neu thieu category thi gan mac dinh la Khac
                if "category" not in row or row["category"] == "":
                    row["category"] = "Khác"

                # Them dong vao danh sach giao dich
                transactions.append(row)

        # Tra ve danh sach giao dich
        return transactions

    # Ham tao ID moi tu dong tang
    def create_new_id(self):
        # Lay toan bo giao dich
        transactions = self.get_all_transactions()

        # Neu chua co giao dich nao thi ID dau tien la 1
        if len(transactions) == 0:
            return 1

        # Lay danh sach ID hop le
        ids = [int(transaction["id"]) for transaction in transactions if str(transaction.get("id", "")).isdigit()]

        # Neu khong co ID hop le thi bat dau tu 1
        if len(ids) == 0:
            return 1

        # Tra ve ID moi bang ID lon nhat cong 1
        return max(ids) + 1

    # Ham them giao dich moi
    def add_transaction(self, transaction_type, date, description, amount, category):
        # Tao ID moi
        new_id = self.create_new_id()

        # Mo file CSV o che do them du lieu
        with open(self.file_path, mode="a", newline="", encoding="utf-8-sig") as file:
            # Tao doi tuong writer
            writer = csv.writer(file)

            # Ghi giao dich moi vao file
            writer.writerow([new_id, transaction_type, date, description, amount, category])

    # Ham sua giao dich theo ID
    def update_transaction(self, transaction_id, transaction_type, date, description, amount, category):
        # Lay danh sach giao dich hien tai
        transactions = self.get_all_transactions()

        # Duyet tung giao dich
        for transaction in transactions:
            # Neu dung ID can sua
            if transaction["id"] == str(transaction_id):
                transaction["type"] = transaction_type
                transaction["date"] = date
                transaction["description"] = description
                transaction["amount"] = amount
                transaction["category"] = category
                break

        # Ghi lai file CSV
        self.save_all_transactions(transactions)

    # Ham xoa giao dich theo ID
    def delete_transaction(self, transaction_id):
        # Lay danh sach giao dich hien tai
        transactions = self.get_all_transactions()

        # Giu lai nhung giao dich khong trung ID can xoa
        new_transactions = [transaction for transaction in transactions if transaction["id"] != str(transaction_id)]

        # Ghi lai file CSV
        self.save_all_transactions(new_transactions)

    # Ham ghi lai toan bo du lieu vao file CSV
    def save_all_transactions(self, transactions):
        # Mo file CSV o che do ghi lai tu dau
        with open(self.file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            # Tao doi tuong DictWriter
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            # Ghi dong tieu de
            writer.writeheader()

            # Duyet tung giao dich
            for transaction in transactions:
                # Chi ghi cac cot can thiet de tranh loi du cot
                writer.writerow({
                    "id": transaction.get("id", ""),
                    "type": transaction.get("type", ""),
                    "date": transaction.get("date", ""),
                    "description": transaction.get("description", ""),
                    "amount": transaction.get("amount", "0"),
                    "category": transaction.get("category", "Khác") or "Khác"
                })

    # Ham chuyen so tien tu chuoi sang so thuc
    def to_float(self, value):
        # Thu chuyen du lieu sang so
        try:
            return float(str(value).replace(",", "").strip())
        except ValueError:
            return 0

    # Ham chuyen chuoi ngay dd/mm/yyyy sang datetime
    def parse_date(self, date_text):
        # Thu doc ngay theo dinh dang cua chuong trinh
        try:
            return datetime.strptime(date_text, "%d/%m/%Y")
        except ValueError:
            return None

    # Ham tinh tong thu nhap
    def get_total_income(self):
        # Lay toan bo giao dich
        transactions = self.get_all_transactions()

        # Cong cac giao dich co loai Thu nhap
        return sum(self.to_float(t["amount"]) for t in transactions if t["type"] == "Thu nhập")

    # Ham tinh tong chi tieu
    def get_total_expense(self):
        # Lay toan bo giao dich
        transactions = self.get_all_transactions()

        # Cong cac giao dich co loai Chi tieu
        return sum(self.to_float(t["amount"]) for t in transactions if t["type"] == "Chi tiêu")

    # Ham tinh so du con lai
    def get_balance(self):
        # So du bang tong thu tru tong chi
        return self.get_total_income() - self.get_total_expense()

    # Ham tim kiem giao dich theo tu khoa, loai, danh muc, khoang ngay va khoang tien
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
        # Lay toan bo danh sach giao dich
        transactions = self.get_all_transactions()

        # Chuyen tu khoa ve chu thuong de tim kiem khong phan biet hoa thuong
        keyword = keyword.lower().strip()

        # Chuyen cac thong so bo loc thanh gia tri de so sanh
        date_from_dt = self.parse_date(date_from) if date_from else None
        date_to_dt = self.parse_date(date_to) if date_to else None
        min_amount_val = self.to_float(min_amount) if min_amount not in (None, "") else None
        max_amount_val = self.to_float(max_amount) if max_amount not in (None, "") else None

        # Tao danh sach ket qua
        results = []

        # Duyet tung giao dich
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

    # Ham thong ke chi tieu theo danh muc
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

    # Ham tinh ty le phan tram chi tieu theo danh muc
    def get_expense_percentage_by_category(self, transactions=None):
        expenses = self.get_expenses_by_category(transactions)
        total_expense = sum(expenses.values())

        if total_expense == 0:
            return {category: (amount, 0.0) for category, amount in expenses.items()}

        return {
            category: (amount, round(amount / total_expense * 100, 2))
            for category, amount in expenses.items()
        }

    # Ham thong ke chi tieu theo thang
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

