"""A small in-memory address book with CSV export and JSON backups."""

import csv
import hashlib
import json
import re

contacts = {}


def add_contact(full_name, phone, email="", city="Unknown"):
    """Add a contact when the phone number contains exactly ten digits."""
    if not re.fullmatch(r"[0-9]{10}", phone):
        print("Invalid phone number for", full_name)
        return False
    contacts[full_name] = {"phone": phone, "email": email, "city": city}
    return True


def contact_id(full_name):
    """Return a short, deterministic identifier for a contact name."""
    return hashlib.sha256(full_name.encode("utf-8")).hexdigest()[:6]


def search_contacts(query):
    """Find contact names matching a name fragment or phone fragment."""
    query_lower = query.lower()
    return [
        name
        for name, info in contacts.items()
        if query_lower in name.lower() or query in info["phone"]
    ]


def update_city(full_name, city):
    """Update a contact's city, returning False when the contact is missing."""
    contact = contacts.get(full_name)
    if contact is None:
        print("No contact named", full_name)
        return False
    contact["city"] = city
    return True


def contacts_by_city():
    """Group contact names by their current city."""
    grouped = {}
    for name, info in contacts.items():
        grouped.setdefault(info["city"], []).append(name)
    return grouped


def print_directory():
    """Print contacts in alphabetical order."""
    for index, name in enumerate(sorted(contacts), start=1):
        print(index, name, contacts[name]["phone"])


def export_csv(file_name="contacts.csv"):
    """Export the address book as CSV rows."""
    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["city"]])


def backup_book(file_name="contacts.json"):
    """Write a JSON backup that does not execute code when loaded."""
    with open(file_name, "w", encoding="utf-8") as backup_file:
        json.dump(contacts, backup_file, indent=2, sort_keys=True)


def restore_book(file_name="contacts.json"):
    """Restore a JSON backup and validate its top-level structure."""
    with open(file_name, "r", encoding="utf-8") as backup_file:
        restored = json.load(backup_file)
    if not isinstance(restored, dict):
        raise ValueError("Backup must contain a JSON object.")
    for name, info in restored.items():
        if not isinstance(name, str) or not isinstance(info, dict):
            raise ValueError("Backup contains an invalid contact entry.")
        if not {"phone", "email", "city"}.issubset(info):
            raise ValueError("Backup contact is missing required fields.")
    return restored


def main():
    """Run a small demonstration of address-book features."""
    add_contact("Neha Sharma", "9876543210", "neha@example.com", "Bengaluru")
    add_contact("Rahul Verma", "9123456780", "rahul@example.com", "Mysuru")
    add_contact("Test User", "12345")
    add_contact("Kavya Nair", "9988776655", city="Bengaluru")
    update_city("Rahul Verma", "Chennai")
    update_city("Nobody", "Delhi")
    print_directory()
    print("Search 'ra':", search_contacts("ra"))
    print("By city:", contacts_by_city())
    print("Id for Neha:", contact_id("Neha Sharma"))
    export_csv()
    backup_book()
    restored = restore_book()
    print("Contacts restored:", len(restored), "| first:", sorted(restored)[0])
    print(
        "Restored contacts match the in-memory address book:",
        restored == contacts,
    )


if __name__ == "__main__":
    main()
