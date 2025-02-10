import random
import json
import os

def generate_building_rules():
    """Generate a set of structured rules for complex string construction and reduction."""
    return [
        ("AB", "BA"),
        ("CA", "AC"),
        ("CB", "BC"),
        ("ABCABC", "")  # Collapse everything at the end
    ]

def build_complex_string(rules):
    """Build a complex string step by step, ensuring it can be reduced to an empty string."""
    # Step 1: Create a base string with several "ABCABC" sequences
    current_string = "".join(["ABCABC" for _ in range(random.randint(2, 5))])
    steps = []

    # Step 2: Add additional random substrings and transformations
    additional_parts = ["CB", "AB", "CA"] * random.randint(1, 3)
    random.shuffle(additional_parts)
    current_string += "".join(additional_parts)

    # Step 3: Record unique transitions
    applied_rules = set()
    for rule in rules:
        if rule[0] in current_string and rule not in applied_rules:
            steps.append({"src": rule[0], "tgt": rule[1]})
            applied_rules.add(rule)

    return current_string, steps

def generate_puzzles(num_puzzles=10, output_dir="advanced_puzzles"):
    """Generate multiple advanced puzzles and save them as JSON files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    rules = generate_building_rules()
    
    for i in range(num_puzzles):
        problem_id = f"{i + 210:03}"
        initial_string, transitions = build_complex_string(rules)
        
        puzzle = {
            "problem_id": problem_id,
            "initial_string": initial_string,
            "transitions": transitions
        }
        
        with open(os.path.join(output_dir, f"puzzle_{problem_id}.json"), "w") as f:
            json.dump(puzzle, f, indent=4)

# Generate 10 advanced puzzles
generate_puzzles()
