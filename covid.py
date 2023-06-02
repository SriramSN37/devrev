import json

vaccination_centres = []
users = []
admin_password = "admin123"

def save_data():
    data = {
        "vaccination_centres": vaccination_centres,
        "users": users
    }
    with open("data.json", "w") as file:
        json.dump(data, file)

def load_data():
    global vaccination_centres, users
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            vaccination_centres = data["vaccination_centres"]
            users = data["users"]
    except FileNotFoundError:
        pass

def login():
    username = input("Username: ")
    password = input("Password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def user_signup():
    username = input("Username: ")
    password = input("Password: ")

    user = {
        "username": username,
        "password": password
    }
    users.append(user)
    save_data()
    print("User registered successfully.")

def search_vaccination_centres():
    print("Vaccination Centres:")
    for centre in vaccination_centres:
        print("Name:", centre["name"])
        print("Location:", centre["location"])
        print("Working Hours:", centre["working_hours"])
        print("Slots Available:", centre["slots_available"])
        print()

def apply_vaccination_slot(user):
    centre_name = input("Enter Vaccination Centre Name: ")
    for centre in vaccination_centres:
        if centre["name"] == centre_name:
            if centre["slots_available"] > 0:
                centre["slots_available"] -= 1
                save_data()
                print("Vaccination slot applied successfully.")
                return
            else:
                print("No slots available for this centre.")
                return
    print("Invalid centre name.")

def admin_login():
    password = input("Enter Admin Password: ")
    if password == admin_password:
        return True
    else:
        print("Invalid password.")
        return False

def add_vaccination_centre():
    if admin_login():
        name = input("Enter Centre Name: ")
        location = input("Enter Centre Location: ")
        working_hours = input("Enter Working Hours: ")
        slots_available = int(input("Enter Slots Available: "))

        centre = {
            "name": name,
            "location": location,
            "working_hours": working_hours,
            "slots_available": slots_available
        }
        vaccination_centres.append(centre)
        save_data()
        print("Vaccination centre added successfully.")

def get_dosage_details():
    if admin_login():
        dosage_details = {}
        for centre in vaccination_centres:
            dosage_details[centre["name"]] = centre["slots_available"]
        print("Dosage Details:")
        for centre, dosage in dosage_details.items():
            print("Centre:", centre)
            print("Dosage Available:", dosage)
            print()

def remove_vaccination_centre():
    if admin_login():
        centre_name = input("Enter Centre Name to remove: ")
        for centre in vaccination_centres:
            if centre["name"] == centre_name:
                vaccination_centres.remove(centre)
                save_data()
                print("Vaccination centre removed successfully.")
                return
        print("Invalid centre name.")

def main():
    load_data()
    while True:
        print("==== Covid Vaccination Booking ====")
        print("1. Login")
        print("2. Sign up")
        print("3. Search Vaccination Centres")
        print("4. Apply for Vaccination Slot")
        print("5. Admin Login")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = login()
            if user:
                print("Logged in successfully as", user["username"])
                # User specific actions
                while True:
                    print("==== User Actions ====")
                    print("1. Search Vaccination Centres")
                    print("2. Apply for Vaccination Slot")
                    print("3. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        search_vaccination_centres()
                    elif user_choice == "2":
                        apply_vaccination_slot(user)
                    elif user_choice == "3":
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid username or password.")

        elif choice == "2":
            user_signup()

        elif choice == "3":
            search_vaccination_centres()

        elif choice == "4":
            print("Login to apply for vaccination slot.")
            user = login()
            if user:
                apply_vaccination_slot(user)
            else:
                print("Invalid username or password.")

        elif choice == "5":
            admin_login()
            if admin_login():
                # Admin specific actions
                while True:
                    print("==== Admin Actions ====")
                    print("1. Add Vaccination Centre")
                    print("2. Get Dosage Details")
                    print("3. Remove Vaccination Centre")
                    print("4. Logout")
                    admin_choice = input("Enter your choice: ")
                    if admin_choice == "1":
                        add_vaccination_centre()
                    elif admin_choice == "2":
                        get_dosage_details()
                    elif admin_choice == "3":
                        remove_vaccination_centre()
                    elif admin_choice == "4":
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid password.")

        elif choice == "6":
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
