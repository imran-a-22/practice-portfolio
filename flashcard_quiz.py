#!/usr/bin/env python3
"""
Flashcard Quiz (Python)
A small terminal-based ed-tech program for revision practice.

Run:
    python3 flashcard_quiz.py
"""

from dataclasses import dataclass
import random


@dataclass
class Question:
    prompt: str
    choices: list[str]
    answer_index: int
    explanation: str


QUESTIONS = [
    Question(
        prompt="What is 12 x 8?",
        choices=["86", "96", "108", "88"],
        answer_index=1,
        explanation="12 multiplied by 8 equals 96.",
    ),
    Question(
        prompt="Which planet is known as the Red Planet?",
        choices=["Mars", "Venus", "Jupiter", "Mercury"],
        answer_index=0,
        explanation="Mars is called the Red Planet because of iron oxide on its surface.",
    ),
    Question(
        prompt="What is the main idea of photosynthesis?",
        choices=[
            "Plants use sunlight to make food",
            "Plants breathe only at night",
            "Plants turn rocks into water",
            "Plants use roots to make fire",
        ],
        answer_index=0,
        explanation="Photosynthesis is the process plants use to make glucose using sunlight, water, and carbon dioxide.",
    ),
    Question(
        prompt="Which punctuation mark ends a direct question?",
        choices=["Comma", "Full stop", "Question mark", "Colon"],
        answer_index=2,
        explanation="Questions end with a question mark.",
    ),
    Question(
        prompt="What is 3/4 written as a decimal?",
        choices=["0.25", "0.5", "0.75", "1.25"],
        answer_index=2,
        explanation="3 divided by 4 is 0.75.",
    ),
]


def ask_question(question: Question, number: int) -> bool:
    print(f"\nQuestion {number}: {question.prompt}")
    labels = ["A", "B", "C", "D"]
    for label, choice in zip(labels, question.choices):
        print(f"  {label}. {choice}")

    while True:
        user_input = input("Your answer (A/B/C/D): ").strip().upper()
        if user_input in labels:
            selected_index = labels.index(user_input)
            is_correct = selected_index == question.answer_index
            if is_correct:
                print("Correct!")
            else:
                correct_label = labels[question.answer_index]
                correct_choice = question.choices[question.answer_index]
                print(f"Not quite. Correct answer: {correct_label}. {correct_choice}")
            print(f"Explanation: {question.explanation}")
            return is_correct
        print("Please type A, B, C, or D.")


def main() -> None:
    print("Welcome to Flashcard Quiz!")
    print("You will answer 5 mixed-subject revision questions.")

    questions = QUESTIONS[:]
    random.shuffle(questions)

    score = 0
    for i, question in enumerate(questions, start=1):
        if ask_question(question, i):
            score += 1

    percent = (score / len(questions)) * 100
    print("\n--- Results ---")
    print(f"Score: {score}/{len(questions)}")
    print(f"Percentage: {percent:.0f}%")

    if percent == 100:
        print("Excellent work.")
    elif percent >= 60:
        print("Good job. Keep revising and you will improve even more.")
    else:
        print("Solid start. Review the explanations and try again.")


if __name__ == "__main__":
    main()
