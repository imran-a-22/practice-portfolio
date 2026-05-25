# program title a computer science quiz in python :)

# Data used in the program - declaring variables
questions = 10 # amount of questions every quiz run 
question_index = 0 # controls which question is shown
score = 0 # tracks how many answers were correct
total_questions = len(questions) # measures the amount of questions
user_response_1 = input().strip().lower() # tracks user responses to general q's
quiz_answer = input().strip().lower() # tracks user responses to quiz q's

# own functions made for the program
start_quiz(){ # function to start the quiz
    0
}

# loop to request input until user responds correctly for a typical user_response
while True:
    user_response_1 = input("Are you ready to begin the quiz? (Yes or No)").strip().lower()
    if user_response_1 == "yes":
        print("Starting quiz...")
        # start_quiz_function()
        break 
    elif user_response_1 == "no":
        print("Exiting...")
        break
    else:
        print("Error: Please type 'yes' or 'no'.")


# Main quiz loop
for in: 
    0 
    # check answer
        # if quiz_answer is correct
            # print 'correct!'
            # add +1 to score
            # add 1 to question_index

        # if quiz_answer is wrong
            # print 'incorrect!'
            # print correct question answer option + explanation
            # add 1 to question_index