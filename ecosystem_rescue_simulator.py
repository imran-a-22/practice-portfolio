import random

SPECIES = {
    "plants": {"min": 40, "max": 100},
    "rabbits": {"min": 15, "max": 60},
    "foxes": {"min": 5, "max": 20},
}

ACTIONS = {
    "1": {
        "name": "Restore meadow",
        "effect": {"plants": 18, "rabbits": 4, "foxes": 0},
        "lesson": "Producers like plants support the whole food chain.",
    },
    "2": {
        "name": "Protect rabbit nests",
        "effect": {"plants": -4, "rabbits": 10, "foxes": 2},
        "lesson": "Helping prey species also affects predator numbers later.",
    },
    "3": {
        "name": "Reduce pollution",
        "effect": {"plants": 10, "rabbits": 5, "foxes": 3},
        "lesson": "Healthier habitats raise survival rates across multiple species.",
    },
    "4": {
        "name": "Observe and skip",
        "effect": {"plants": 0, "rabbits": 0, "foxes": 0},
        "lesson": "Observation matters, but no intervention means nature keeps shifting on its own.",
    },
}


def clamp_species(state):
    for species, limits in SPECIES.items():
        state[species] = max(0, min(state[species], limits["max"] + 30))


def ecosystem_status(state):
    stable = True
    messages = []
    for species, limits in SPECIES.items():
        amount = state[species]
        if amount < limits["min"]:
            stable = False
            messages.append(f"{species.title()} are too low.")
        elif amount > limits["max"]:
            stable = False
            messages.append(f"{species.title()} are too high.")
    if stable:
        messages.append("The ecosystem is balanced.")
    return stable, messages


def apply_natural_shift(state):
    state["plants"] += random.randint(-8, 8)
    state["rabbits"] += random.randint(-6, 6)
    state["foxes"] += random.randint(-3, 3)
    clamp_species(state)


def ask_choice():
    while True:
        print("Choose an action:")
        for key, action in ACTIONS.items():
            print(f"  {key}. {action['name']}")
        choice = input("Action: ").strip()
        if choice in ACTIONS:
            return choice
        print("Invalid choice. Enter 1, 2, 3, or 4.\n")


def main():
    state = {"plants": 35, "rabbits": 22, "foxes": 9}
    score = 0
    print("=== Ecosystem Rescue Simulator ===")
    print("Balance plants, rabbits, and foxes over 6 seasons.\n")

    for season in range(1, 7):
        print(f"Season {season}")
        print(f"Plants: {state['plants']} | Rabbits: {state['rabbits']} | Foxes: {state['foxes']}")
        stable, messages = ecosystem_status(state)
        for message in messages:
            print("-", message)

        action = ACTIONS[ask_choice()]
        for species, change in action["effect"].items():
            state[species] += change
        clamp_species(state)
        apply_natural_shift(state)

        print(action["lesson"])
        stable, _ = ecosystem_status(state)
        if stable:
            score += 15
            print("Balanced season. +15 score.\n")
        else:
            print("The food web still needs work.\n")

    print("Final score:", score)
    final_stable, final_messages = ecosystem_status(state)
    for message in final_messages:
        print("-", message)
    print("Great restoration work." if final_stable else "Try another run and stabilise the biome faster.")


if __name__ == "__main__":
    main()
