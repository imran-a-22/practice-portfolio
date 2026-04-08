import random
from dataclasses import dataclass


@dataclass
class Question:
    prompt: str
    options: list[str]
    answer: int
    explanation: str


QUESTIONS = [
    Question(
        prompt="Choose the closest meaning to 'resilient'.",
        options=["fragile", "able to recover quickly", "silent", "careless"],
        answer=1,
        explanation="Resilient means able to recover quickly after difficulty.",
    ),
    Question(
        prompt="Choose the closest meaning to 'scarce'.",
        options=["rare or limited", "easy to find", "bright", "extremely loud"],
        answer=0,
        explanation="Scarce means there is not much of something available.",
    ),
    Question(
        prompt="Choose the best antonym of 'expand'.",
        options=["stretch", "grow", "shrink", "improve"],
        answer=2,
        explanation="Expand means grow larger, so the antonym is shrink.",
    ),
    Question(
        prompt="Choose the closest meaning to 'precise'.",
        options=["messy", "exact", "temporary", "mysterious"],
        answer=1,
        explanation="Precise means exact and accurate.",
    ),
    Question(
        prompt="Choose the best antonym of 'ancient'.",
        options=["old", "historic", "modern", "stone"],
        answer=2,
        explanation="Ancient refers to something very old, so modern is the opposite.",
    ),
    Question(
        prompt="Choose the closest meaning to 'observe'.",
        options=["ignore", "watch carefully", "erase", "argue"],
        answer=1,
        explanation="Observe means to watch or notice carefully.",
    ),
    Question(
        prompt="Choose the closest meaning to 'reluctant'.",
        options=["eager", "unwilling", "powerful", "friendly"],
        answer=1,
        explanation="Reluctant means unwilling or hesitant.",
    ),
    Question(
        prompt="Choose the best antonym of 'benefit'.",
        options=["advantage", "profit", "harm", "reward"],
        answer=2,
        explanation="Benefit is something helpful, while harm is damaging.",
    ),
    Question(
        prompt="Choose the closest meaning to 'combine'.",
        options=["separate", "join together", "hide", "measure"],
        answer=1,
        explanation="Combine means to join things together.",
    ),
    Question(
        prompt="Choose the closest meaning to 'vivid'.",
        options=["dull", "bright and clear", "thin", "broken"],
        answer=1,
        explanation="Vivid means bright, strong, and easy to imagine.",
    ),
]

ENEMIES = [
    ("Goblin of Guesswork", 22),
    ("Ogre of Confusion", 28),
    ("Shadow of Weak Vocabulary", 34),
    ("Archive Dragon", 40),
]


def ask_choice(max_option: int) -> int:
    while True:
        choice = input("Your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= max_option:
            return int(choice) - 1
        print(f"Enter a number between 1 and {max_option}.")


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer yes or no.")


def draw_bar(label: str, current: int, maximum: int) -> None:
    width = 20
    filled = max(0, min(width, round(width * current / maximum)))
    print(f"{label:<8} [{'#' * filled}{'-' * (width - filled)}] {current}/{maximum}")


def battle_enemy(enemy_name: str, enemy_hp_max: int, questions: list[Question]) -> tuple[bool, int, int]:
    player_hp_max = 30
    player_hp = player_hp_max
    enemy_hp = enemy_hp_max
    combo = 0
    score = 0
    used = 0
    potion_available = True

    print(f"\nA wild {enemy_name} appears!\n")

    question_pool = questions[:]
    random.shuffle(question_pool)

    while player_hp > 0 and enemy_hp > 0 and question_pool:
        q = question_pool.pop()
        used += 1
        print("-" * 58)
        draw_bar("Hero", player_hp, player_hp_max)
        draw_bar(enemy_name[:8], enemy_hp, enemy_hp_max)
        print(f"Combo: {combo}   Score: {score}")
        print(f"\n{q.prompt}")
        for i, option in enumerate(q.options, start=1):
            print(f"  {i}. {option}")

        choice = ask_choice(len(q.options))
        if choice == q.answer:
            combo += 1
            damage = 6 + combo
            enemy_hp = max(0, enemy_hp - damage)
            score += 10 + combo * 2
            print(f"\nCorrect. You cast Word Strike for {damage} damage!")
        else:
            combo = 0
            damage = random.randint(4, 8)
            player_hp = max(0, player_hp - damage)
            print(f"\nIncorrect. The right answer was: {q.options[q.answer]}")
            print(f"{enemy_name} hits you for {damage} damage.")

        print(q.explanation)

        if player_hp > 0 and potion_available and player_hp <= 12:
            use_potion = ask_yes_no("Use your healing potion for +8 HP? (y/n): ")
            if use_potion:
                potion_available = False
                player_hp = min(player_hp_max, player_hp + 8)
                print("You restore 8 HP. Stay focused.")

    won = enemy_hp <= 0
    return won, score, used


def main() -> None:
    print("=" * 58)
    print("WORD WIZARD DUEL")
    print("Defeat monsters by choosing the correct word meaning.")
    print("Correct answers build combo damage. One potion per battle.")
    print("=" * 58)

    total_score = 0
    total_questions = 0
    victories = 0

    for enemy_name, hp in ENEMIES:
        won, score, used = battle_enemy(enemy_name, hp, QUESTIONS)
        total_score += score
        total_questions += used
        if won:
            victories += 1
            print(f"\nYou defeated {enemy_name}!\n")
        else:
            print(f"\nYou were defeated by {enemy_name}. Study, then try again.\n")
            break

    print("=" * 58)
    print("RUN SUMMARY")
    print(f"Victories: {victories}/{len(ENEMIES)}")
    print(f"Questions answered: {total_questions}")
    print(f"Final score: {total_score}")
    if victories == len(ENEMIES):
        print("You cleared the Vocabulary Tower.")
    elif victories >= 2:
        print("Strong run. Your vocabulary power is improving.")
    else:
        print("Keep training. Small consistent practice wins.")
    print("=" * 58)


if __name__ == "__main__":
    main()
