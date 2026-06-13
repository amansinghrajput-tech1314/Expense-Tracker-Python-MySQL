class Expense:
    """Domain Model representing an Expense transaction entry."""
    def __init__(self, expense_id, user_id, amount, category, description, date, created_at=None):
        self.id = expense_id
        self.user_id = user_id
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date
        self.created_at = created_at