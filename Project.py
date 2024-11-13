import bcrypt
import getpass

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = self.hash_password(password)  # Store hashed password
        self.role = role

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)


class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }


class InventorySystem:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.current_user = None
        self.add_user("admin", "admin123", "admin")

    def add_user(self, username, password, role):
        self.users[username] = User(username, password, role)

    def login(self, username, password):
        if username in self.users:
            user = self.users[username]
            if user.check_password(password):
                self.current_user = user
                return True
        return False

    def logout(self):
        self.current_user = None

    def add_product(self, product_id, name, category, price, stock_quantity):
        self.products[product_id] = Product(product_id, name, category, price, stock_quantity)

    def view_products(self):
        return [product.to_dict() for product in self.products.values()]


def main():
    inventory_system = InventorySystem()

    while True:
        if not inventory_system.current_user:
            print("\n1. Login\n2. Add User (Role: user)\n3. Exit(admin,admin 123 FOR ADMIN LOGIN)")
            choice = input("Enter your choice: ")

            if choice == "1":
                username = input("Username: ")
                password = getpass.getpass("Password: ")
                if inventory_system.login(username, password):
                    print(f"Welcome, {username}!")
                else:
                    print("Invalid username or password")
            elif choice == "2":
                username = input("Username: ")
                password = getpass.getpass("Password: ")
                # Automatically set the role to 'user'
                role = "user"
                inventory_system.add_user(username, password, role)
                print("User added successfully!")
            elif choice == "3":
                break
            else:
                print("Invalid choice")
        else:
            if inventory_system.current_user.role == "admin":
                # Admin view
                print("\n1. View products\n2. Add product\n3. Add user (Role: user)\n4. Logout\n5. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    products = inventory_system.view_products()
                    for product in products:
                        print(f"ID: {product['product_id']}, Name: {product['name']}, Price: ${product['price']}, Stock: {product['stock_quantity']}")
                elif choice == "2":
                    product_id = input("Product ID: ")
                    name = input("Name: ")
                    category = input("Category: ")
                    price = float(input("Price: "))
                    stock_quantity = int(input("Stock Quantity: "))
                    inventory_system.add_product(product_id, name, category, price, stock_quantity)
                    print("Product added successfully!")
                elif choice == "3":
                    username = input("Username: ")
                    password = getpass.getpass("Password: ")
                    role = "user"
                    inventory_system.add_user(username, password, role)
                    print("User added successfully!")
                elif choice == "4":
                    inventory_system.logout()
                    print("Logged out successfully!")
                elif choice == "5":
                    break
                else:
                    print("Invalid choice")
            else:
                # Option for users
                print("\n1. View products\n2. Logout\n3. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    products = inventory_system.view_products()
                    for product in products:
                        print(f"ID: {product['product_id']}, Name: {product['name']}, Price: ${product['price']}, Stock: {product['stock_quantity']}")
                elif choice == "2":
                    inventory_system.logout()
                    print("Logged out successfully!")
                elif choice == "3":
                    break
                else:
                    print("Invalid choice")

main()

