import os
import csv

from helpers.csv_helper import find_max_id, load_questions, validate_file 


def main():
    # Since locations are set as constants, must delete the files before running the tests
    test_validate_file()
    test_load_questions()
    test_find_max_id()


def test_validate_file():
    headers = ["id", "name"]
    file_path = "data/test_profiles.csv"
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    assert not os.path.exists(file_path)
    result = validate_file(file_path, headers)
    assert result is False
    assert os.path.exists(file_path)
    
    result = validate_file(file_path, headers)
    assert result is True
    
    os.remove(file_path)

def test_load_questions():
    file_path = "data/questions.csv"
    
    if os.path.exists(file_path):
        os.remove(file_path)

    headers = ["id", "title", "answer", "enabled", "choices"]
    with open(file_path, "w") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerow({"id": 1, "title": "Test Question", "answer": "a", "enabled": "True", "choices": ""})
    
    questions = load_questions()
    assert len(questions) == 1
    assert questions[0].id == 1
    assert questions[0].title == "Test Question"
    assert questions[0].answer == "a"
    assert questions[0].enabled == True
    
    os.remove(file_path)
    
def test_find_max_id():
    file_path = "data/test_.csv"
    headers = ["id", "name"]

    # Create a sample file
    import csv
    with open(file_path, "w") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerow({"id": "1", "name": "First"})
        writer.writerow({"id": "3", "name": "Third"})
        writer.writerow({"id": "2", "name": "Second"})

    # Verify max ID
    max_id = find_max_id("id", file_path)
    assert max_id == 3

    # Clean up
    import os
    os.remove(file_path)

if __name__ == "__main__":
    main()
    
    