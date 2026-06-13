import sys
from datetime import datetime
from tabulate import tabulate

from services.auth_service import AuthService
from services.income_service import IncomeService
from services.expense_service import ExpenseService
from config import EXPENSE_CATEGORIES

class ApplicationConsoleUI:
    """Core Orchestrator driving User Interactions and state routing."""
    def __init__(self):
        self.auth_service = AuthService()
        self.income_service = IncomeService()
        self.expense_service = ExpenseService()
        self.current_user = None

    def clear_screen(self):
        print("\n" + "="*60 + "\n")

    def read_numeric(self, prompt):
        while True:
            try:
                val = float(input(prompt).strip())
                if val <= 0:
                    print("[!] Value must be greater than zero.")
                    continue
                return val
            except ValueError:
                print("[!] Input validation error: Enter a structural floating number.")

    def read_date(self, prompt):
        while True:
            date_in = input(prompt).strip()
            if not date_in:
                return datetime.today().strftime('%Y-%m-%d')
            try:
                datetime.strptime(date_in, '%Y-%m-%d')
                return date_in
            except ValueError:
                print("[!] Date violation: String format must map to YYYY-MM-DD.")

    def display_dashboard(self):
        self.clear_screen()
        u_id = self.current_user.id
        total_in = self.income_service.get_total_income(u_id)
        total_out = self.expense_service.get_total_expense(u_id)
        net_balance = total_in - total_out

        print(f"=== FINANCIAL DASHBOARD (User: {self.current_user.username}) ===")
        dashboard_data = [
            ["Total Registered Inflow", f"${total_in:,.2f}"],
            ["Total Registered Outflow", f"${total_out:,.2f}"],
            ["Net Operational Capital", f"${net_balance:,.2f}"]
        ]
        print(tabulate(dashboard_data, headers=["Metric Indicator", "Valuation Value"], tablefmt="fancy_grid"))

        print("\n[Top Expenditure Metrics]")
        analytics = self.expense_service.get_category_analytics(u_id)[:3]
        if analytics:
            print(tabulate([[a['category'], f"${a['total']:,.2f}"] for a in analytics], headers=["Category", "Total Spent"], tablefmt="simple"))
        else:
            print("No categorical analytical points tracked yet.")

    def auth_loop(self):
        while True:
            print("\n::: EXPENSE TRACKER ARCHITECT SUITE :::")
            print("1. Account Initialization (Register)")
            print("2. Authentication Checkpoint (Login)")
            print("3. Terminate Routine")
            choice = input("Enter System Code Action: ").strip()

            if choice == '1':
                user = input("Choose System Username: ").strip()
                passwd = input("Choose Cryptographic Password: ").strip()
                success, msg = self.auth_service.register_user(user, passwd)
                print(f"[*] Status: {msg}")
            elif choice == '2':
                user = input("Identify Username: ").strip()
                passwd = input("Verification Password: ").strip()
                account, msg = self.auth_service.login_user(user, passwd)
                if account:
                    self.current_user = account
                    print(f"\n[+] Authorization Confirmed. System greeting: Session initialised.")
                    self.application_loop()
                else:
                    print(f"\n[!] Error Handled: {msg}")
            elif choice == '3':
                print("\n[-] Dismantling thread contexts. Application gracefully exit.")
                sys.exit(0)
            else:
                print("[!] Command Unknown. Select a valid system option.")

    def application_loop(self):
        while True:
            self.display_dashboard()
            print("\n--- OPERATIONAL SUBSYSTEM CONTROLS ---")
            print("1. Ingest Income Stream")
            print("2. Ingest Expense Item")
            print("3. Display Structural Ledger Statements")
            print("4. Mutation Interface (Update Existing Expense)")
            print("5. Deletion Interface (Purge Record)")
            print("6. Unified Multi-Entity Search Query")
            print("7. Sector Analytical breakdown Reports")
            print("8. Archive Dataset to Flat-file (CSV)")
            print("9. Flush Account Context (Logout)")
            
            sub_choice = input("\nExecute Subsystem Code: ").strip()
            u_id = self.current_user.id

            if sub_choice == '1':
                amt = self.read_numeric("Enter Net Liquidity Amount: ")
                src = input("Income Resource Origin: ").strip()
                desc = input("Contextual Annotation: ").strip()
                dt = self.read_date("Context Chronology [YYYY-MM-DD / Enter for today]: ")
                _, msg = self.income_service.add_income(u_id, amt, src, desc, dt)
                print(msg)

            elif sub_choice == '2':
                amt = self.read_numeric("Enter Expense Value Charged: ")
                print("Available Categories: " + ", ".join(EXPENSE_CATEGORIES))
                cat = input("Map Category Definition: ").strip()
                if cat not in EXPENSE_CATEGORIES:
                    print("[!] Structural Constraint Abort: Non-supported catalog item allocation.")
                    continue
                desc = input("Line-item Context Description: ").strip()
                dt = self.read_date("Context Chronology [YYYY-MM-DD / Enter for today]: ")
                _, msg = self.expense_service.add_expense(u_id, amt, cat, desc, dt)
                print(msg)

            elif sub_choice == '3':
                self.clear_screen()
                print("=== DETAILED HISTORICAL TRANSACTION REGISTER ===")
                expenses = self.expense_service.get_all_expenses(u_id)
                incomes = self.income_service.get_all_income(u_id)
                
                print("\n[Income Sub-Ledger]")
                if incomes:
                    print(tabulate([[i['id'], f"${i['amount']:,.2f}", i['source'], i['description'], i['date']] for i in incomes], headers=["ID", "Amount", "Source", "Description", "Date"], tablefmt="psql"))
                else: print("No recorded dynamic income vectors.")

                print("\n[Expense Sub-Ledger]")
                if expenses:
                    print(tabulate([[e['id'], f"${e['amount']:,.2f}", e['category'], e['description'], e['date']] for e in expenses], headers=["ID", "Amount", "Category", "Description", "Date"], tablefmt="psql"))
                else: print("No recorded outflow tracking records.")
                input("\nPress [Enter] to return to interface control loops...")

            elif sub_choice == '4':
                exp_id = int(self.read_numeric("Provide Targeted Transaction ID: "))
                amt = self.read_numeric("Input Modified Absolute Nominal Value: ")
                cat = input("New Target Categorization Category: ").strip()
                desc = input("Update Annotation Memo: ").strip()
                dt = self.read_date("Update Target Allocation Date [YYYY-MM-DD]: ")
                _, msg = self.expense_service.update_expense(u_id, exp_id, amt, cat, desc, dt)
                print(msg)

            elif sub_choice == '5':
                print("1. Purge Income Entry  2. Purge Expense Entry")
                del_type = input("Choose Operation Target Class: ")
                target_id = int(self.read_numeric("Provide Row Primary Key to purge: "))
                if del_type == '1':
                    _, msg = self.income_service.delete_income(u_id, target_id)
                else:
                    _, msg = self.expense_service.delete_expense(u_id, target_id)
                print(msg)

            elif sub_choice == '6':
                kw = input("Enter Regex/String Token Keyword query parameter: ").strip()
                matches = self.expense_service.search_transactions(u_id, kw)
                if matches:
                    print(tabulate([[m['type'], m['id'], f"${m['amount']:,.2f}", m['metric'], m['description'], m['date']] for m in matches], headers=["Type", "ID", "Value", "Sector/Origin", "Meta", "Date"], tablefmt="grid"))
                else:
                    print("[*] Scan finished. Null array records evaluated against target argument token.")
                input("\nControl paused. Return via [Enter].")

            elif sub_choice == '7':
                self.clear_screen()
                print("=== ADVANCED FINANCIAL ANALYTICS ===")
                cats = self.expense_service.get_category_analytics(u_id)
                print("\n[Category Volumetric Cost Distribution Summary]")
                print(tabulate([[c['category'], f"${c['total']:,.2f}"] for c in cats], headers=["Category Allocation", "Combined Outflow Value"], tablefmt="fancy_grid"))
                
                months = self.expense_service.get_monthly_summary(u_id)
                print("\n[Temporal Monthly Operational Trajectory Tracking]")
                print(tabulate([[m['month'], f"${m['total']:,.2f}"] for m in months], headers=["Chronological Term", "Aggregate Spend Valuation"], tablefmt="fancy_grid"))
                input("\nAnalytics processed. Exit via [Enter].")

            elif sub_choice == '8':
                _, msg = self.expense_service.export_to_csv(u_id)
                print(msg)
                input("\nIO execution completed. Press Enter.")

            elif sub_choice == '9':
                self.current_user = None
                print("\n[*] Context dropped. Security token context cleared.")
                break

if __name__ == "__main__":
    app = ApplicationConsoleUI()
    try:
        app.auth_loop()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupt Vector triggered. Secure application thread safely halted.")
        sys.exit(0)