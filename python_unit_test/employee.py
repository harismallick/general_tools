import requests

class Employee:

    raise_amount: float = 1.05

    def __init__(self, first: str, last: str, pay: float) -> None:
        self.first: str = first
        self.last: str = last
        self.pay: float = pay

    @property
    def email(self) -> str:
        return f"{self.first.lower()}.{self.last.lower()}@company.com"
    
    @property
    def fullname(self) -> str:
        return f"{self.first} {self.last}"
    
    def apply_raise(self) -> None:
        self.pay = int(self.pay * self.raise_amount)


    def monthly_schedule(self, month):
        response = requests.get(f'http://company.com/{self.last}/{month}')
        if response.ok:
            return response.text
        else:
            return 'Bad Response!'