import sys
import os
import csv
from tabulate import tabulate
from dataclasses import dataclass
from typing import List, Tuple
from enums.mode import ModeEnum
from helpers import user_input_helper
from models.question_statistics import QuestionStatistics
from models.profile import Profile
from models.question import Question
import helpers.csv_helper as csv_helper
import helpers.question_helper as question_helper
import random

def main():
    print("Welcome to Quizly!")
    questions = csv_helper.load_questions()
    # Use default profile until player selects or creates another profile
    profile = csv_helper.load_profile_with_statistics("default")
    profile.init_statistics(questions)

    while True:
        print(f"Current Profile: '{profile.name}', id: {profile.id}")
        try:
            mode = user_input_helper.select_mode()
            match mode:
                case ModeEnum.ADD_QUESTIONS:
                    add_questions(questions)
                    profile.init_statistics(questions)
                case ModeEnum.VIEW_STATISTICS:
                    view_statistics(questions, profile)
                case ModeEnum.ENABLE_OR_DISABLE_QUESTIONS:
                    enable_or_disable_questions(questions)
                case ModeEnum.PRACTICE_MODE:
                    practice_mode(profile, questions)
                case ModeEnum.TEST_MODE:
                    test_mode(profile, questions)
                case ModeEnum.SELECT_PROFILE:
                    profile = select_profile(profile)
                    profile.init_statistics(questions)
                case ModeEnum.QUIT:
                    print("Saving...")
                    csv_helper.save_questions(questions)
                    csv_helper.save_question_statistics(profile)
                    sys.exit("\nThanks for playing!")
        except KeyboardInterrupt:
            print("\nSaving...")
            csv_helper.save_questions(questions)
            csv_helper.save_question_statistics(profile)
            sys.exit("\nThanks for playing!")
    
def add_questions(questions: List[Question]) -> None:
    print("Please provide following details to add new questions.\n")
    
    # In case there were no questions in the file, start ids from 0
    previous_count = len(questions)
    if previous_count == 0:
        highest_id = 0
    else:
        highest_id = 0
        for question in questions:
            highest_id = max(highest_id, question.id)
        
    while True:
        try:
            print(f"Question {highest_id + 1}.")
            
            question_type = user_input_helper.get_question_type()
            
            if question_type == '1':
                title = input("Title: ").capitalize().strip()
                answer = input("Answer: ").strip()
                choices = []
                for i in range(2):
                    choices.append(input(f"Choice {i + 1}: ").strip())
                
                if not title or not answer or not all(choices):
                    print("Title, Answer or Choices can not be empty! Please try again. \n")
                    continue
                else:
                    questions.append(Question(highest_id, title, answer, choices=choices))
            
            elif question_type == '2':
                title = input("Title: ").capitalize().strip()
                answer = input("Answer: ").strip()

                if not title or not answer:
                    print("Title or Answer can not be empty! Please try again. \n")
                    continue
                else:
                    questions.append(Question(highest_id, title, answer))
                
            highest_id += 1
                
            while True:
                decision = input("Would you like to enter another question? [y/n]: ").strip().lower()
                if decision == 'n':
                    print(f"Exiting. Successfully added {len(questions) - previous_count} new question(s)! \n")
                    return questions
                elif decision == 'y':
                    print()
                    break
                else:
                    print("Please enter either 'y' or 'n'.")
                    continue
        
        except KeyboardInterrupt:
            print(f"Exiting. Successfully added {len(questions) - previous_count} new questions!")
            return questions
                
def view_statistics(questions: List[Question], profile: Profile) -> None:
    print("\nWelcome to Statistics View!")
    
    if len(questions) == 0:
        print("Unable to view statistics if no questions are found!\n")
        return
    
    order = user_input_helper.get_order_type()
    
    print(f"Displaying statistics for '{profile.name}' profile...")
    
    data = []
    for q in questions:
        stat = profile.get_statistics_for_question(q.id)
        if stat.times_answered != 0:
            score = round(stat.times_answered_correctly / stat.times_answered * 100)
        else:
            score = 0
        data.append([
            q.id,
            q.title,
            q.answer,
            q.enabled,
            score
        ])

    reverse_order = order == "descending"
    # Using lambda, sort by score
    data.sort(key=lambda x: x[4], reverse=reverse_order)

    columns = ["Question ID", "Title", "Answer", "Enabled", "Score (%)"]
    print(tabulate(data, headers=columns, tablefmt="grid"))
    print()

def enable_or_disable_questions(questions: List[Question]) -> None:
    if len(questions) == 0:
        print("Unable to enable/disable questions if no questions are found!\n")
        return questions
    
    data = [[q.id, q.title, q.answer, q.enabled] for q in questions]
    columns = ["Question ID", "Title", "Answer", "Enabled"]
    print(tabulate(data, headers=columns, tablefmt="grid"))
    
    print("\nPlease select ID of a question you wish to disable/enable.")
    while True:
        try:
            question_id = int(input("ID: "))
        except ValueError:
            print("Invalid ID! Try again.")
            continue
        
        index = -1
        for i, q in enumerate(questions):
            if q.id == question_id:
                q.enabled = not q.enabled
                index = i
                break
        
        if index == -1:
            print("Invalid ID! Try again.")
            continue
        
        print(f"\nSuccessfully changed question {question_id} enabled status!\n")
        print(tabulate([data[index]], headers=columns, tablefmt="grid"))
        print()
        return
    
def practice_mode(profile: Profile, questions: List[Question]) -> None:
    print("\nWelcome to Practice Mode!")
    if len(questions) < 5:
        print("Please create at least 5 questions before starting Practice Mode.\n")
        return
    
    enabled_count = 0
    for q in questions:
        enabled_count += 1 if q.enabled else 0
    
    if enabled_count < 5:
        print("Please enable at least 5 questions before starting Practice Mode.\n")
        return
    
    
    while True:
        print("If you wish to quit, type 'quit'.\n")
        
        question = question_helper.get_random_questions(profile, questions)[0]
        correct_answer = question.answer
        print(f"Question: {question.title}")
        
        if question.is_quiz():
            # creating a copy here to not alter question.choices itself
            choices = question.choices.copy()
            choices.append(correct_answer)
        
            random.shuffle(choices)

            print("Choices: ")
            print("A: ", choices[0])
            print("B: ", choices[1])
            print("C: ", choices[2])

            answer_input = user_input_helper.get_user_test_answer()
            if answer_input == "quit":
                print("Exiting...")
                return print("You can view your statistics in Statistics View!\n")

            # Get the answer from the choices list
            user_answer = choices['abc'.index(answer_input)]
        else:        
            user_answer = input("Answer: ").strip()
            
            if user_answer == "quit":
                print("Exiting...")
                return print("You can view your statistics in Statistics View!\n")

        if user_answer.lower() == correct_answer.lower():    
            print("\nCorrect!\n")
            profile.get_statistics_for_question(question.id).update_statistics(True)
        else:
            print(f"\nIncorrect! Correct answer: {correct_answer}\n")
            profile.get_statistics_for_question(question.id).update_statistics(False)
    
def test_mode(profile: Profile, questions: List[Question]) -> None:
    print("\nWelcome to Test Mode!")
    
    if len(questions) < 5:
        return print("Please create at least 5 questions before starting Practice Mode.\n")
    
    enabled_count = 0
    for q in questions:
        enabled_count += 1 if q.enabled else 0
    
    try:
        question_count = int(input("Please enter the amount of questions in the test: "))
    except ValueError:
        print("Invalid number! Try again.")
    
    if enabled_count < question_count:
        return print(f"Please enable at least {enabled_count - question_count} questions before starting Test Mode.\n")
        
    total_questions = len(questions)
    if question_count > total_questions:
        print(f"\nQuestion bank contains {total_questions} questions.")
        return print(f"Please add at least {question_count - total_questions} more question(s) to create a test of such size.\n")
    
    random.shuffle(questions)
    test_questions = questions[:question_count]
    correct_answers = 0
    for question in test_questions:
        print("If you wish to quit, type 'quit'.\n")

        correct_answer = question.answer
        print(f"Question: {question.title}")
        
        if question.is_quiz():
            # creating a copy here to not alter question.choices itself
            choices = question.choices.copy()
            choices.append(correct_answer)
            random.shuffle(choices)
            
            print("Choices: ")
            print("A: ", choices[0])
            print("B: ", choices[1])
            print("C: ", choices[2])
        
            answer_input = user_input_helper.get_user_test_answer()
            if answer_input == "quit":
                print("Exiting...")
                return print("You can view your statistics in Statistics View!\n")

            # Get the answer from the choices list
            user_answer = choices['abc'.index(answer_input)]
        else:
            user_answer = input("Answer: ").strip()
            
            if user_answer == "quit":
                print("Exiting...")
                return print("You can view your statistics in Statistics View!\n")
        
        if user_answer.lower() == correct_answer.lower():    
            print("\nCorrect!\n")
            correct_answers += 1
            profile.get_statistics_for_question(question.id).update_statistics(True)
        else:
            print(f"\nIncorrect! Correct answer: {correct_answer}\n")
            profile.get_statistics_for_question(question.id).update_statistics(False)
        
    print(f"Test completed! You answered {correct_answers} out of {question_count} questions correctly!\n")
    
def select_profile(profile: Profile) -> Profile:
    choice = user_input_helper.select_profile()

    if profile and profile.question_statistics:
        print("Saving current profile question statistics...\n")
        csv_helper.save_question_statistics(profile)

    if choice == "select":
        print("Loading available profiles...\n")
        profiles = csv_helper.load_profile_names()
        
        if len(profiles) <= 1:
            print("Please add more profiles before selecting!\n")
            return profile
        
        data = [[profile.id, profile.name] for profile in profiles]
        columns = ["Profile ID", "Name"]
        
        print(tabulate(data, columns, tablefmt="grid"))
        
        print("\nPlease type the ID of the profile you would like to select.")
        while True:
            try:
                profile_id = int(input("ID: "))
            except ValueError:
                print("Invalid ID selected! Try again.\n")
                continue
            
            new_profile = None
            for p in profiles:
                if p.id == profile_id:
                    # Load profile with statistics
                    new_profile = csv_helper.load_profile_statistics(Profile(p.id, p.name, None))
                    break
                
            if not new_profile:
                print("Invalid ID selected! Try again.\n")
                continue
            
            print(f"You successfully selected profile: {profile.name.title()}!\n")
            return new_profile
    else:
        profile_id = csv_helper.find_profile_max_id()
        while True:
            name = input("Enter new profile name: ").strip().lower()
            new_profile = Profile(profile_id + 1, name, None)
            if not csv_helper.create_new_profile(new_profile):
                print("Please enter a name which has not been used before.\n")
            else: 
                print(f"Successfully created a new profile {name.title()}!\n")
                return new_profile
    

if __name__ == "__main__":
    main()
    
# Part 3 repository: 
# https://github.com/algirdasleo/OOP-practice-game-War