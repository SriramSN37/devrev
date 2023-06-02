import json
import requests
import mysql.connector

# MySQL connection details
db_host = '33'
db_user = 'root'  # Replace with your MariaDB username
db_password = 'subi1234'  # Replace with your MariaDB password
db_name = 'covid_vaccination'

# API endpoint URLs
base_url = 'http://127.0.0.1:5000'
signup_url = base_url + '/users/signup'
login_url = base_url + '/users/login'
centres_url = base_url + '/centres'
apply_url = base_url + '/centres/apply'

# Initialize MySQL connection
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = connection.cursor()

# Load data from MySQL tables into memory
vaccination_centres = []
users = []


def save_data():
    # Save data to MySQL tables
    # Save vaccination_centres to the 'vaccination_centres' table
    cursor.execute('DELETE FROM vaccination_centres')
    for centre in vaccination_centres:
        sql = 'INSERT INTO vaccination_centres (name, location, working_hours, slots_available) ' \
              'VALUES (%s, %s, %s, %s)'
        values = (centre['name'], centre['location'], centre['working_hours'], centre['slots_available'])
        cursor.execute(sql, values)
    connection.commit()

    # Save users to the 'users' table
    cursor.execute('DELETE FROM users')
    for user in users:
        sql = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        values = (user['username'], user['password'])
        cursor.execute(sql, values)
    connection.commit()


def load_data():
    # Load data from MySQL tables into memory
    cursor.execute('SELECT * FROM vaccination_centres')
    centres_data = cursor.fetchall()
    for centre_data in centres_data:
        centre = {
            'name': centre_data[1],
            'location': centre_data[2],
            'working_hours': centre_data[3],
            'slots_available': centre_data[4]
        }
        vaccination_centres.append(centre)

    cursor.execute('SELECT * FROM users')
    users_data = cursor.fetchall()
    for user_data in users_data:
        user = {
            'username': user_data[1],
            'password': user_data[2]
        }
        users.append(user)


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
    response = requests.get(centres_url)
    if response.status_code == 200:
        centres = response.json()
        print("Vaccination Centres:")
        for centre in centres:
            print("Name:", centre["name"])
            print("Location:", centre["location"])
            print("Working Hours:", centre["working_hours"])
            print("Slots Available:", centre["slots_available"])
            print()
    else:
        print("Error occurred while fetching vaccination centres.")


def apply_vaccination_slot(user):
    centre_name = input("Enter Vaccination Centre Name: ")
    payload = {
        "centre_name": centre_name,
        "username": user["username"]
    }
    response = requests.post(apply_url, json=payload)
    if response.status_code == 200:
        print("Vaccination slot applied successfully.")
    else:
        print("Error occurred while applying for the vaccination slot.")


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
        response = requests.get(centres_url)
        if response.status_code == 200:
            centres = response.json()
            print("Dosage Details:")
            for centre in centres:
                print("Centre:", centre["name"])
                print("Dosage Available:", centre["slots_available"])
                print()
        else:
            print("Error occurred while fetching dosage details.")


def remove_vaccination_centre():
    if admin_login():
        centre_name = input("Enter Centre Name to remove: ")
        response = requests.delete(centres_url + '/' + centre_name)
        if response.status_code == 200:
            print("Vaccination centre removed successfully.")
        else:
            print("Error occurred while removing the vaccination centre.")


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
            print("Login to apply for a vaccination slot.")
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
                print("Invalid admin password.")

        elif choice == "6":
            save_data()
            break

        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()
