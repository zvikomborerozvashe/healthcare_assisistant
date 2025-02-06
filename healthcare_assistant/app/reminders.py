import json
import os
from datetime import datetime, timedelta

REMINDERS_FILE = "reminders.json"

def load_reminders():
    """Loads reminders from a JSON file."""
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as file:
            return json.load(file)
    return []

def save_reminders(reminders):
    """Saves reminders to a JSON file."""
    with open(REMINDERS_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

def add_reminder():
    """Prompts the user to enter a reminder and saves it."""
    message = input("Enter reminder message: ")
    try:
        time_offset = int(input("In how many minutes? "))
        reminder_time = datetime.now() + timedelta(minutes=time_offset)
        reminders = load_reminders()
        reminders.append({"message": message, "time": reminder_time.strftime("%Y-%m-%d %H:%M:%S")})
        save_reminders(reminders)
        print(f"Reminder set: '{message}' at {reminder_time.strftime('%H:%M:%S')}")
    except ValueError:
        print("Invalid input. Please enter a number for time.")

def list_reminders():
    """Lists all active reminders."""
    reminders = load_reminders()
    if not reminders:
        print("No reminders set.")
    else:
        print("\nYour reminders:")
        for index, reminder in enumerate(reminders, start=1):
            print(f"{index}. {reminder['message']} - {reminder['time']}")

def remove_reminder():
    """Prompts user to remove a reminder by index."""
    list_reminders()
    reminders = load_reminders()
    if reminders:
        try:
            index = int(input("\nEnter the reminder number to remove: "))
            if 1 <= index <= len(reminders):
                removed = reminders.pop(index - 1)
                save_reminders(reminders)
                print(f"Removed reminder: '{removed['message']}'")
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Enter a number.")

def check_reminders():
    """Checks for due reminders and notifies the user."""
    reminders = load_reminders()
    now = datetime.now()
    updated_reminders = []
    
    for reminder in reminders:
        reminder_time = datetime.strptime(reminder["time"], "%Y-%m-%d %H:%M:%S")
        if reminder_time <= now:
            print(f"🔔 Reminder: {reminder['message']}")
        else:
            updated_reminders.append(reminder)
    
    save_reminders(updated_reminders)

def reminders_menu():
    """Provides a menu interface for managing reminders."""
    while True:
        print("\n📌 Reminder Manager")
        print("1. Add Reminder")
        print("2. List Reminders")
        print("3. Remove Reminder")
        print("4. Check Reminders")
        print("5. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            add_reminder()
        elif choice == "2":
            list_reminders()
        elif choice == "3":
            remove_reminder()
        elif choice == "4":
            check_reminders()
        elif choice == "5":
            print("Exiting Reminder Manager...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the menu when the script is executed
if __name__ == "__main__":
    reminders_menu()
