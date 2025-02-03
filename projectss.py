from pymongo import MongoClient

# MongoDB connection (Replace URI with your MongoDB connection string)
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["restaurant"]
dishes_collection = db["dishes"]

# Functions for CRUD operations
def add_dish():
    try:
        name = input("Enter dish name: ").strip()
        price = input("Enter dish price: ")
        while not price.replace('.', '', 1).isdigit():
            print("Invalid price! Please enter a numeric value.")
            price = input("Enter dish price: ")
        price = float(price)

        category = input("Enter dish category: ").strip()
        available = input("Is the dish available? (yes/no): ").strip().lower()
        while available not in ["yes", "no"]:
            print("Invalid input! Please enter 'yes' or 'no'.")
            available = input("Is the dish available? (yes/no): ").strip().lower()

        dish = {
            "name": name,
            "price": price,
            "category": category,
            "available": available == "yes",
        }
        dishes_collection.insert_one(dish)
        print("Dish added successfully!")
    except Exception as e:
        print(f"Error adding dish: {e}")

def view_dishes():
    print("\n--- Available Dishes ---")
    try:
        dishes = dishes_collection.find()
        for i, dish in enumerate(dishes, start=1):
            print(
                f"{i}. Name: {dish.get('name', 'N/A')}, Price: ₹{dish.get('price', 'N/A')}, "
                f"Category: {dish.get('category', 'N/A')}, Available: {dish.get('available', 'N/A')}"
            )
    except Exception as e:
        print(f"Error fetching dishes: {e}")

def update_dish():
    try:
        dish_name = input("Enter the name of the dish to update: ").strip()
        dish = dishes_collection.find_one({"name": dish_name})

        if dish:
            print("Leave fields empty to keep the current value.")
            new_name = input(f"Enter new name [{dish['name']}]: ").strip() or dish["name"]
            
            new_price = input(f"Enter new price [{dish['price']}]: ").strip()
            new_price = float(new_price) if new_price else dish["price"]
            
            new_category = input(f"Enter new category [{dish['category']}]: ").strip() or dish["category"]
            
            new_available = input(f"Is the dish available? (yes/no) [{dish['available']}]: ").strip().lower()
            if new_available not in ["", "yes", "no"]:
                print("Invalid input! Keeping the current availability status.")
                new_available = dish["available"]
            else:
                new_available = dish["available"] if new_available == "" else new_available == "yes"

            updated_dish = {
                "name": new_name,
                "price": new_price,
                "category": new_category,
                "available": new_available,
            }

            dishes_collection.update_one({"_id": dish["_id"]}, {"$set": updated_dish})
            print("Dish updated successfully!")
        else:
            print("Dish not found!")
    except Exception as e:
        print(f"Error updating dish: {e}")

def delete_dish():
    try:
        dish_name = input("Enter the name of the dish to delete: ").strip()
        result = dishes_collection.delete_one({"name": dish_name})
        if result.deleted_count > 0:
            print("Dish deleted successfully!")
        else:
            print("Dish not found!")
    except Exception as e:
        print(f"Error deleting dish: {e}")

# Main Menu
def main_menu():
    while True:
        print("\n--- Restaurant Management ---")
        print("1. Add Dish")
        print("2. View Dishes")
        print("3. Update Dish")
        print("4. Delete Dish")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_dish()
        elif choice == "2":
            view_dishes()
        elif choice == "3":
            update_dish()
        elif choice == "4":
            delete_dish()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
