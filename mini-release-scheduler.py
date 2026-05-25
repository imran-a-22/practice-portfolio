# main.py

from collections import defaultdict


def read_input():
    print("Mini Release Scheduler")
    print("----------------------")
    print("You will enter tasks using this format:")
    print("taskId hours priority dependencyCount dep1 dep2 dep3...")
    print("Example: api 4 5 1 database")
    print()

    working_hours = int(input("Enter working hours available per day: ").strip())
    total_tasks = int(input("Enter total number of tasks: ").strip())

    tasks = {}

    print()
    print("Now enter each task.")
    print("Format: taskId hours priority dependencyCount dep1 dep2 dep3...")
    print()

    for task_number in range(1, total_tasks + 1):
        task_input = input(f"Enter task {task_number} of {total_tasks}: ").strip()
        parts = task_input.split()

        task_id = parts[0]
        hours = int(parts[1])
        priority = int(parts[2])
        dependency_count = int(parts[3])

        dependencies = parts[4:4 + dependency_count]

        tasks[task_id] = {
            "hours": hours,
            "priority": priority,
            "dependencies": dependencies
        }

    return working_hours, tasks


def build_dependency_data(tasks):
    remaining_dependencies = {}
    dependents = defaultdict(list)

    for task_id, task_data in tasks.items():
        dependencies = task_data["dependencies"]
        remaining_dependencies[task_id] = len(dependencies)

        for dependency in dependencies:
            dependents[dependency].append(task_id)

    return remaining_dependencies, dependents


def get_initial_available_tasks(remaining_dependencies):
    available_tasks = []

    for task_id, dependency_count in remaining_dependencies.items():
        if dependency_count == 0:
            available_tasks.append(task_id)

    return available_tasks


def select_best_task(available_tasks, tasks):
    available_tasks.sort(
        key=lambda task_id: (
            -tasks[task_id]["priority"],
            tasks[task_id]["hours"],
            task_id
        )
    )

    return available_tasks[0]


def create_schedule(working_hours, tasks):
    remaining_dependencies, dependents = build_dependency_data(tasks)
    available_tasks = get_initial_available_tasks(remaining_dependencies)

    schedule = []
    current_day = []
    remaining_hours = working_hours

    completed_count = 0
    total_tasks = len(tasks)

    while completed_count < total_tasks:

        if len(available_tasks) == 0:
            return None

        selected_task = select_best_task(available_tasks, tasks)
        selected_task_hours = tasks[selected_task]["hours"]

        if selected_task_hours > working_hours:
            print("TASK TOO LARGE")
            return "TASK_TOO_LARGE"

        if selected_task_hours > remaining_hours:
            if current_day:
                schedule.append(current_day)

            current_day = []
            remaining_hours = working_hours
            continue

        current_day.append(selected_task)
        remaining_hours -= selected_task_hours

        available_tasks.remove(selected_task)
        completed_count += 1

        for dependent_task in dependents[selected_task]:
            if dependent_task in remaining_dependencies:
                remaining_dependencies[dependent_task] -= 1

                if remaining_dependencies[dependent_task] == 0:
                    available_tasks.append(dependent_task)

    if current_day:
        schedule.append(current_day)

    return schedule


def print_schedule(schedule):
    print()
    print("Final Schedule")
    print("--------------")

    if schedule is None:
        print("CYCLE DETECTED")
        return

    if schedule == "TASK_TOO_LARGE":
        return

    for index, day in enumerate(schedule, start=1):
        print(f"Day {index}: {' '.join(day)}")


def main():
    working_hours, tasks = read_input()
    schedule = create_schedule(working_hours, tasks)
    print_schedule(schedule)

main()