import random
import string
import json
import os

def generate_random_string(min_length=3, max_length=8):
    """Generate a random string of length between min_length and max_length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(min_length, max_length)))

def generate_initial_rule():
    """Generate the first rule that maps an empty string to a non-empty string."""
    return {"src": "", "tgt": generate_random_string()}

def generate_subsequent_rules(starting_string, num_rules=5, max_attempts=10):
    """Generate additional rules that transform substrings of the starting string."""
    rules = []
    current_string = starting_string
    seen_substrings = set()
    attempts = 0

    while len(rules) < num_rules and attempts < max_attempts:
        if len(current_string) < 3:
            break  # No more meaningful substrings to replace

        # Select a random substring to replace
        start = random.randint(0, len(current_string) - 2)
        end = random.randint(start + 1, min(start + 5, len(current_string)))
        old = current_string[start:end]

        if old in seen_substrings:
            attempts += 1
            continue  # Avoid duplicates

        new = generate_random_string()
        current_string = current_string.replace(old, new, 1)  # Replace only the first occurrence
        rules.append({"src": old, "tgt": new})
        seen_substrings.add(old)
        attempts = 0  # Reset attempts after a successful rule generation

    return current_string, rules

def reverse_rules(rules):
    """Reverse each rule in the list."""
    return [{"src": rule["tgt"], "tgt": rule["src"]} for rule in rules]

def generate_puzzles(num_puzzles=50, output_dir="sed_puzzles"):
    """Generate multiple sed-like puzzles and save them as JSON files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    generated_count = 0
    while generated_count < num_puzzles:
        # Step 1: Generate the first rule that maps "" to a non-empty string
        initial_rule = generate_initial_rule()
        initial_string = initial_rule["tgt"]

        # Step 2: Generate subsequent transformation rules
        num_additional_rules = random.randint(3, 6)
        final_string, additional_rules = generate_subsequent_rules(initial_string, num_additional_rules)

        # Step 3: Ensure the minimum number of transitions
        if len(additional_rules) < 3:
            continue  # Skip if not enough transitions

        # Step 4: Reverse all rules to transform the final string back to an empty string
        all_rules = [initial_rule] + additional_rules
        reversed_rules = reverse_rules(all_rules)

        # Step 5: Create the puzzle with the final string as the initial string
        problem_id = f"{generated_count + 100:03}"
        puzzle = {
            "problem_id": problem_id,
            "initial_string": final_string,  # This is now the starting string
            "transitions": reversed_rules    # Reversed rules guarantee transformation to an empty string
        }
        
        with open(os.path.join(output_dir, f"puzzle_{problem_id}.json"), "w") as f:
            json.dump(puzzle, f, indent=4)
        
        generated_count += 1
        print(f"Generated puzzle {problem_id}")

# Generate 100 sed-like puzzles
generate_puzzles()
