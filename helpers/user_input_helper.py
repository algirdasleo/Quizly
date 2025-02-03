from enums.mode import ModeEnum

def select_mode() -> ModeEnum:
    print("Please select a mode by entering a number (1 - 7):")
    for enum in ModeEnum:
        print(f"{enum.value}. {" ".join(enum.name.capitalize().split("_"))}")
    
    print()
    selected_mode = None
    while selected_mode == None:
        try:
            mode_num = int(input("Mode (1 - 7): "))
            selected_mode = ModeEnum(mode_num)
        except ValueError:
            print("Invalid number! Please select again.")
            continue
    print(f"Successfully selected Mode {selected_mode.value}: {" ".join(selected_mode.name.capitalize().split("_"))}!")
    print()
    return selected_mode

def select_profile() -> str:
    print("Would you like to select available profiles or create a new one?")
    while True:
        choice = input("Type 'select' or 'create': ").strip().lower()
        if choice not in ["select", "create"]:
            print("Invalid choice! Please try again.\n")
            continue
        break
    return choice

def get_user_test_answer() -> str:
    while True:
        user_answer = input("Your answer: ").strip().lower()
        
        if user_answer == "quit":
            return "quit"
        
        if user_answer in ['a', 'b', 'c']:
            return user_answer
        else:
            print("Invalid choice! Please try again.\n")

def get_order_type() -> str:
    while True:
        order = input("Sort questions by score 'ascending' or 'descending'?: ").lower().strip()
        if order not in ["ascending", "descending"]:
            print("Invalid ordering type! Please enter: 'ascending' or 'descending'.")
            continue
        break
    return order

def get_question_type() -> str:
    while True:
        question_type = input("Please enter the type of question (1 for Quiz, 2 for Free-Form): ").strip()
        if question_type not in ['1', '2']:
            print("Invalid input! Please enter either '1' or '2'.")
            continue
        break
    
    return question_type