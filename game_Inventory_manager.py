# A standard game inventory system made in Python :)
# By Imran A.

from dataclasses import dataclass


ALLOWED_ITEM_TYPES = ["Weapon", "Potion", "Armor", "Quest Item", "Material"]


@dataclass
class InventoryItem:
    # Master blueprint for all items
    name: str
    quantity: int
    item_type: str


class PlayerInventory:
    # Master blueprint to hold all items together

    def __init__(self):
        self.items = {}

    def add_item(self, item: InventoryItem):
        item_key = item.name.lower()

        if item_key in self.items:
            self.items[item_key].quantity += item.quantity
            print(f"{item.name} quantity increased successfully.")
        else:
            self.items[item_key] = item
            print(f"{item.name} added successfully.")

    def remove_item(self, item_name):
        item_key = item_name.lower()

        if item_key in self.items:
            del self.items[item_key]
            print(f"{item_name} removed successfully.")
        else:
            print("Item not found.")

    def use_item(self, item_name):
        item_key = item_name.lower()

        if item_key not in self.items:
            print("Item not found.")
            return

        self.items[item_key].quantity -= 1
        print(f"You used one {self.items[item_key].name}.")

        if self.items[item_key].quantity <= 0:
            print(f"{self.items[item_key].name} has run out and was removed.")
            del self.items[item_key]

    def view_inventory(self):
        if len(self.items) == 0:
            print("Inventory is empty.")
            return

        print("\nPlayer Inventory:")
        counter = 1

        for item in self.items.values():
            print(f"{counter}. {item.name} | Quantity: {item.quantity} | Type: {item.item_type}")
            counter += 1


def read_user_input(message):
    return input(message).strip()


def print_to_screen(message):
    print(message)


def input_validation(value, validation_type):
    if validation_type == "quantity":
        return value.isdigit() and int(value) > 0

    if validation_type == "item_type":
        return value.title() in ALLOWED_ITEM_TYPES

    return False


def show_menu():
    print("\n1. View Inventory")
    print("2. Add Item")
    print("3. Use Item")
    print("4. Remove Item")
    print("5. Exit")


def view_inventory(player_inventory):
    player_inventory.view_inventory()


def add_item(player_inventory):
    item_name = read_user_input("Enter item name: ")

    quantity_input = read_user_input("Enter quantity: ")

    if not input_validation(quantity_input, "quantity"):
        print("Invalid quantity. Please enter a positive number.")
        return

    print("\nAllowed item types:")
    for item_type in ALLOWED_ITEM_TYPES:
        print(f"- {item_type}")

    item_type = read_user_input("Enter item type: ").title()

    if item_type not in ALLOWED_ITEM_TYPES:
        print("Invalid item type.")
        return

    new_item = InventoryItem(
        name=item_name,
        quantity=int(quantity_input),
        item_type=item_type
    )

    player_inventory.add_item(new_item)


def remove_item(player_inventory):
    item_name = read_user_input("Enter item name to remove: ")
    player_inventory.remove_item(item_name)


def use_item(player_inventory):
    item_name = read_user_input("Enter item name to use: ")
    player_inventory.use_item(item_name)


def main():
    player_inventory = PlayerInventory()

    print_to_screen("Welcome to the Game Inventory Manager")

    while True:
        show_menu()

        user_choice = read_user_input("Choose an option: ")

        if user_choice == "1":
            view_inventory(player_inventory)

        elif user_choice == "2":
            add_item(player_inventory)

        elif user_choice == "3":
            use_item(player_inventory)

        elif user_choice == "4":
            remove_item(player_inventory)

        elif user_choice == "5":
            print("Exiting inventory manager. Goodbye.")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()