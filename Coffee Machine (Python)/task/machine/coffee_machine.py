# Write your code here
class CoffeeMachine:
    def __init__(self, **kwargs: int):
        """
        Creates an instance of the class using either default values
        or values passed to the instance.
        :param kwargs: Any custom amounts we desire as var = value.
        """
        defaults = {'water': 400,
                    'milk': 540,
                    'beans': 120,
                    'till': 550,
                    'paper_cups': 9}
        self.inv = {**defaults, **kwargs}  # The available inventory.

    def remaining(self):
        """
            Prints a formatted report of the machine's contents
            :param inv: dictionary
            :return: None
            """
        print(
            f"""The coffee machine has:
{self.inv['water']} ml of water
{self.inv['milk']} ml of milk
{self.inv['beans']} g of coffee beans
{self.inv['paper_cups']} disposable cups
${self.inv['till']} of money\n"""
        )
        return None

    def fill(self, inv: dict[str, int]) -> dict[str, int]:
        """
        Refills the machine.
        :param inv: The current inventory.
        :return: The updated inventory.
        """
        print('Write how many ml of water you want to add:')
        inv['water'] += int(input())
        print('Write how many ml of milk you want to add:')
        inv['milk'] += int(input())
        print('Write how many grams of coffee beans you want to add:')
        inv['beans'] += int(input())
        print('Write how many disposable cups you want to add:')
        inv['paper_cups'] += int(input())
        print()
        return inv

    def take(self, inv: dict[str, int]) -> dict[str, int]:
        """
        Empties the till.
        :param inv: The current inventory.
        :return: The updated inventory.
        """
        print(f'I gave you ${inv['till']}\n')
        inv['till'] = 0
        return inv

    def buy(self) -> dict[str, int] | None:
        """
        The menu. The user can terminate the transaction with "back".
        :return: Either the order's required ingredients or None.
        """
        print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:')
        match input():
            case '1':
                item = 'espresso'
            case '2':
                item = 'latte'
            case '3':
                item = 'cappuccino'
            case 'back':
                return None
            case _:
                item = 'coffee'

        bill = self.recipe(item)
        return bill

    def recipe(self, item: str, cups: int = 1) -> dict[str, int]:
        """
        Creates the ingredient bill for each choice. These will be
        deducted from the current inventory later.
        :param item: The user's choice. Default is a plain coffee.
        :param cups: The number of paper cups needed. (Default is 1)
        :return: A dictionary of the ingredients needed.
        """
        match item:
            case 'espresso':
                bill = {
                    'water': cups * 250,
                    'milk': cups * 0,
                    'beans': cups * 16,
                    'price': cups * 4
                }
            case 'latte':
                bill = {
                    'water': cups * 350,
                    'milk': cups * 75,
                    'beans': cups * 20,
                    'price': cups * 7
                }
            case 'cappuccino':
                bill = {
                    'water': cups * 200,
                    'milk': cups * 100,
                    'beans': cups * 12,
                    'price': cups * 6
                }
            case _:  # Just make coffee
                bill = {
                    'water': cups * 200,
                    'milk': cups * 50,
                    'beans': cups * 15,
                    'price': cups * 4
                }
        return bill

    def check_inventory(self, bill: dict[str, int], inv: dict[str, int]) -> tuple[bool, str]:
        """
        Checks the order against the available inventory. Fails if an ingredient is
        running too low. Reports that ingredient. (Or a lack of cups!)
        :param bill: The required ingredients.
        :param inv: The available ingredients.
        :return: A tuple of the go/no-go status and the low ingredient.
        """
        common_keys = set(inv.keys()) & set(bill.keys())
        ok = True
        for key in common_keys:
            if bill[key] > inv[key]:
                ok = False
                break
        return ok, key



    def fill_order(self, bill: dict[str, int], inv: dict[str, int]) -> dict[str, int]:
        """
        Deducts the order's ingredients from the machine's inventory and collects the money.
        :param bill: The required ingredients.
        :param inv: The current inventory.
        :return: The updated inventory.
        """
        inv['water'] -= bill['water']
        inv['milk'] -= bill['milk']
        inv['beans'] -= bill['beans']
        inv['paper_cups'] -= 1
        inv['till'] += bill['price']
        return inv

    def take(self, inv: dict[str, int]) -> dict[str, int]:
        """
        Empties the till.
        :param inv: The current inventory.
        :return: The updated inventory.
        """
        print(f'I gave you ${inv['till']}\n')
        inv['till'] = 0
        return inv

if __name__ == '__main__':
    machine = CoffeeMachine()  # Create a CoffeeMachine object.
    action = None  # Create action, but don't give it a value.
    while action != 'exit':  # Loop until the user stops.
        action = input('Write action (buy, fill, take, remaining, exit):\n')
        match action:
            case 'buy':
                bill = machine.buy()  # Show the menu and get the customer's order.
                if bill != None:  # None means the customer canceled the order.
                    check, low_item = machine.check_inventory(bill, machine.inv)
                    # Check the bill of materials against the available inventory.
                    if check:
                        print('I have enough resources, making you a coffee!\n')
                        machine.fill_order(bill, machine.inv)
                    else:
                        print(f'Sorry, not enough {low_item}!\n')
            case 'fill':  # Refill the machine.
                machine.fill(machine.inv)
            case 'remaining':  # Report the inventory.
                machine.remaining()
            case 'take':  # Empty the till.
                machine.take(machine.inv)
            case 'exit':
                exit()
            case _:
                pass
