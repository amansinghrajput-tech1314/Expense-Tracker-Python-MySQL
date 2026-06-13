class Income:
    """Domain Model representing an Income transaction entry."""
    def __init__(self, income_id, user_id, amount, source, description, date, created_at=None):
        self.id = income_id
        self.user_id = user_id
        self.amount = float(amount)
        self.source = source
        self.description = description
        self.date = date
        self.created_at = created_at