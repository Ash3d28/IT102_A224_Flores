from abc import ABC, abstractmethod
import flores_bank_transactions

class BankAccount(ABC):

    def __init__(
        self,
        account_number,
        name,
        pin,
        starting_balance,
        points=0
    ):
        self.account_number = account_number
        self.account_name = name
        self._pin = pin
        self._balance = starting_balance
        self.points = points
        self._reward_deposit_total = 0

    # Encapsulation
    def check_balance(self):
        return self._balance

    def deposit(self, amount):

        if amount <= 0:
            return False

        self._balance += amount

        self.calculate_rewards_points(
            amount
        )

        return True

    def withdraw(self, amount):

        if amount <= 0:
            return False

        if amount > self._balance:
            return False

        self._balance -= amount

        return True

    def verify_pin(self, pin):

        return self._pin == pin

    # Used by storage when the account
    # needs to be saved.
    def get_pin(self):

        return self._pin

    def set_pin(self, pin):

        self._pin = pin

    def get_reward_points(self):

        return self.calculate_rewards_points()

    def calculate_rewards_points(
        self,
        deposit_amount = 0
    ):

        total_deposited = 0
        redeemed_points = 0
        recorded_deposits = False

        for transaction in (
            flores_bank_transactions
            .get_transactions()
        ):

            if (
                transaction.get(
                    "account_number"
                ) == self.account_number
                and
                transaction.get(
                    "transaction"
                ) == "Deposit"
            ):

                recorded_deposits = True
                total_deposited += transaction.get(
                    "amount",
                    0
                )

            elif (
                transaction.get(
                    "account_number"
                ) == self.account_number
                and
                transaction.get(
                    "transaction"
                ) == "Rewards Redemption"
            ):

                redeemed_points += transaction.get(
                    "amount",
                    0
                )

        if recorded_deposits:

            total_deposited += deposit_amount

        else:

            self._reward_deposit_total += deposit_amount
            total_deposited = (
                self._reward_deposit_total
            )

        self.points = int(
            total_deposited // 1000
        ) - int(
            redeemed_points
        )

        if self.points < 0:

            self.points = 0

        return self.points

    def redeem_points_to_balance(
        self,
        points,
        cash_credit
    ):

        if points <= 0 or points > self.points:

            return False

        self.points -= points
        self._balance += cash_credit

        return True

    # Abstraction
    @abstractmethod
    def get_account_type(self):
        pass


# Inheritance
class SavingsAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):

        return "Savings Account"


# Inheritance
class StudentAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):

        return "Student Account"