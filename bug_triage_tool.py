# Bug Triage Tool
# Beginner-friendly Python CLI program


def show_menu():
    print("\n=== Bug Triage Tool ===")
    print("1. Add new bug report")
    print("2. View all bug reports")
    print("3. View open bugs only")
    print("4. Mark bug as resolved")
    print("5. Filter bugs by severity")
    print("6. Sort bugs by severity")
    print("7. Exit")


def get_required_text(prompt):
    while True:
        user_input = input(prompt).strip()

        if user_input == "":
            print("This field cannot be empty. Please try again.")
        else:
            return user_input


def get_valid_severity():
    valid_severities = ["low", "medium", "high", "critical"]

    while True:
        print("\nChoose severity:")
        print("low / medium / high / critical")

        severity = input("Severity: ").strip().lower()

        if severity in valid_severities:
            return severity
        else:
            print("Invalid severity. Please enter low, medium, high, or critical.")


def print_bug(bug):
    print("\n-------------------------")
    print(f"ID: {bug['id']}")
    print(f"Title: {bug['title']}")
    print(f"Description: {bug['description']}")
    print(f"Severity: {bug['severity']}")
    print(f"Reported by: {bug['reported_by']}")
    print(f"Status: {bug['status']}")
    print("-------------------------")


def add_bug(bug_reports, next_bug_id):
    print("\n=== Add New Bug Report ===")

    title = get_required_text("Bug title: ")
    description = get_required_text("Bug description: ")
    severity = get_valid_severity()
    reported_by = get_required_text("Reported by: ")

    bug = {
        "id": next_bug_id,
        "title": title,
        "description": description,
        "severity": severity,
        "reported_by": reported_by,
        "status": "open"
    }

    bug_reports.append(bug)

    print("\nBug entry successfully added!")

    next_bug_id += 1
    return next_bug_id


def view_all_bugs(bug_reports):
    print("\n=== All Bug Reports ===")

    if len(bug_reports) == 0:
        print("No bugs have been reported yet.")
        return

    for bug in bug_reports:
        print_bug(bug)


def view_open_bugs(bug_reports):
    print("\n=== Open Bugs ===")

    open_bugs = []

    for bug in bug_reports:
        if bug["status"] == "open":
            open_bugs.append(bug)

    if len(open_bugs) == 0:
        print("There are currently no open bugs registered.")
        return

    for bug in open_bugs:
        print_bug(bug)


def mark_bug_resolved(bug_reports):
    print("\n=== Mark Bug as Resolved ===")

    if len(bug_reports) == 0:
        print("No bugs have been reported yet.")
        return

    while True:
        bug_id_input = input("Enter the bug ID to mark as resolved: ").strip()

        if not bug_id_input.isdigit():
            print("Please enter a valid number.")
            continue

        bug_id = int(bug_id_input)

        for bug in bug_reports:
            if bug["id"] == bug_id:
                if bug["status"] == "resolved":
                    print("This bug is already resolved.")
                    return

                bug["status"] = "resolved"
                print("Bug successfully updated.")
                return

        print("This bug ID does not exist in the system.")


def filter_bugs_by_severity(bug_reports):
    print("\n=== Filter Bugs by Severity ===")

    if len(bug_reports) == 0:
        print("No bugs have been reported yet.")
        return

    severity = get_valid_severity()

    matching_bugs = []

    for bug in bug_reports:
        if bug["severity"] == severity:
            matching_bugs.append(bug)

    if len(matching_bugs) == 0:
        print(f"No bugs found with severity: {severity}")
        return

    for bug in matching_bugs:
        print_bug(bug)


def sort_bugs_by_severity(bug_reports):
    print("\n=== Sort Bugs by Severity ===")

    if len(bug_reports) == 0:
        print("No bugs have been reported yet.")
        return

    severity_rank = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4
    }

    while True:
        order = input("Do you want ascending or descending order? ").strip().lower()

        if order == "ascending":
            sorted_bugs = sorted(
                bug_reports,
                key=lambda bug: severity_rank[bug["severity"]]
            )
            break

        elif order == "descending":
            sorted_bugs = sorted(
                bug_reports,
                key=lambda bug: severity_rank[bug["severity"]],
                reverse=True
            )
            break

        else:
            print("Please enter either 'ascending' or 'descending'.")

    for bug in sorted_bugs:
        print_bug(bug)


def main():
    bug_reports = []
    next_bug_id = 1

    while True:
        show_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            next_bug_id = add_bug(bug_reports, next_bug_id)

        elif choice == "2":
            view_all_bugs(bug_reports)

        elif choice == "3":
            view_open_bugs(bug_reports)

        elif choice == "4":
            mark_bug_resolved(bug_reports)

        elif choice == "5":
            filter_bugs_by_severity(bug_reports)

        elif choice == "6":
            sort_bugs_by_severity(bug_reports)

        elif choice == "7":
            print("Exiting Bug Triage Tool. Goodbye!")
            break

        else:
            print("Invalid menu option. Please enter a number from 1 to 7.")


main()