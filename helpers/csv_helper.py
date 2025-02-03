import csv
import os
from typing import List
print(os.getcwd())
from models.question_statistics import QuestionStatistics
from models.profile import Profile
from models.question import Question

QUESTIONS_FILE_PATH = "data/questions.csv"
QUESTIONS_STATISTICS_FILE_PATH = "data/questions_statistics.csv"
PROFILES_FILE_PATH = "data/profiles.csv"

def validate_file(file_path: str, expected_headers: List[str]) -> bool:
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_exists = os.path.exists(file_path)
    if file_exists:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            first_line = next(reader, None)
            
            if first_line == expected_headers:
                return True
    
    with open(file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(expected_headers)
    
    return False

def load_questions() -> List[Question]:
    headers = ["id", "title", "answer", "enabled", "choices"]
    
    if not validate_file(QUESTIONS_FILE_PATH, headers):
        return []
    
    questions = []
    with open(QUESTIONS_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        
        for line in reader:
            try:
                choices = line["choices"].split("|") if line["choices"] else []
                questions.append(Question(
                    id = int(line["id"]), 
                    title = line["title"], 
                    answer = line["answer"], 
                    enabled = line["enabled"] == 'True',
                    choices = choices
                ))
            except ValueError:
                print(f"Invalid id found: {line[0]}. Skipping question.")
            except IndexError:
                print(f"Skipping incomplete line: {line}.")
    
    return questions

def create_new_profile(profile: Profile) -> bool:
    headers = ["id", "name"]
    
    validate_file(PROFILES_FILE_PATH, headers)
    
    with open(PROFILES_FILE_PATH) as file:
        reader = csv.DictReader(file)
        for line in reader:
            if line["name"] == profile.name:
                print(f"Profile with name {profile.name} already exists!")
                return False
        
    with open(PROFILES_FILE_PATH, "a") as file:
        writer = csv.DictWriter(file, headers)
        
        new_profile = {
            "id": profile.id,
            "name": profile.name
        }
        writer.writerow(new_profile)
    
    return True

def load_profile_with_statistics(profile_name: str) -> Profile:
    headers = ["id", "name"]
    default_profile = Profile("0", "default", {})
    # If profile file has not been created or is invalid, correct it and return a default profile
    if not validate_file(PROFILES_FILE_PATH, headers):
        create_new_profile(default_profile)
        return default_profile
    
    profile_id = None
    with open(PROFILES_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                if line["name"] == profile_name:
                    profile_id = int(line["id"])
                    break
            except ValueError:
                print(f"Failed to convert data for profile line: {line}")
            except KeyError:
                print(f"Missing data in line: {line}")
    
    # If profile was not found, return default profile
    if profile_id == None:
        return default_profile

    return load_profile_statistics(Profile(profile_id, profile_name, {}))

def load_profile_statistics(profile: Profile) -> Profile:
    headers = ["profile_id", "question_id", "times_answered", "times_answered_correctly", "weight"]
    
    if not validate_file(QUESTIONS_STATISTICS_FILE_PATH, headers):
        return Profile(profile.id, profile.name, {})
    
    # Load the question statistics 
    question_statistics = {}
    with open(QUESTIONS_STATISTICS_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                if int(line["profile_id"]) == profile.id:
                    question_id = int(line["question_id"])
                    question_statistics[question_id] = (QuestionStatistics(
                        times_answered = int(line["times_answered"]),
                        times_answered_correctly = int(line["times_answered_correctly"]),
                        weight = float(line["weight"])
                    ))
            except ValueError:
                print(f"Failed to convert data for question statistics line: {line}")
            except KeyError:
                print(f"Missing data in line: {line}")
    
    return Profile(profile.id, profile.name, question_statistics)

# Loads all profile names from file
def load_profile_names() -> List[Profile]:
    profiles = []
    with open(PROFILES_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            profiles.append(Profile(int(line["id"]), line['name'], {}))
    
    return profiles

def save_questions(questions: List[Question]) -> None:
    headers = ["id", "title", "answer", "enabled", "choices"]
    
    with open(QUESTIONS_FILE_PATH, "w") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(question.to_dict() for question in questions)
    
    print("Successfully saved questions!")

def save_question_statistics(profile: Profile) -> None:
    if not profile.question_statistics:
        return
    
    headers = ["profile_id", "question_id", "times_answered", "times_answered_correctly", "weight"]
    
    validate_file(QUESTIONS_STATISTICS_FILE_PATH, headers)
    
    existing_data = []
    with open(QUESTIONS_STATISTICS_FILE_PATH) as file:
        reader = csv.DictReader(file)
        for line in reader:
            if int(line["profile_id"]) != profile.id:
                existing_data.append({
                    "profile_id": line["profile_id"],
                    "question_id": line["question_id"],
                    "times_answered": line["times_answered"],
                    "times_answered_correctly": line["times_answered_correctly"],
                    "weight": line["weight"]
                })
        
    rows = [
        statistics.to_dict(profile.id, question_id) 
        for question_id, statistics in profile.question_statistics.items()
    ]
    
    rows.extend(existing_data)
    
    with open(QUESTIONS_STATISTICS_FILE_PATH, "w") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print("Successfully saved question statistics!")
    
# Finds the maximum ID in a CSV file
def find_max_id(id_column_name: str, file_path: str) -> int:
    max_id = -1
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                max_id = max(max_id, int(line[id_column_name]))
            except ValueError as e:
                print(f"Invalid column name provided or corrupt file data: {e}")
                continue
                
    return max_id

def find_profile_max_id() -> int:
    return find_max_id("id", PROFILES_FILE_PATH)

def find_questions_max_id() -> int:
    return find_max_id("id", QUESTIONS_FILE_PATH)