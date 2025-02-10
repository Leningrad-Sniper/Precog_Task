import random
import string
import re
import json
import os

def generate_simple_string(length=50, unique_chars=3):
    """Generate a string with a limited set of unique characters to maximize matches."""
    chars = random.choices(string.ascii_letters + string.digits, k=unique_chars)
    return ''.join(random.choice(chars) for _ in range(length))

def generate_effective_rules(min_rules=2, max_rules=5, input_str=""):
    """Generate a small set of distinct substitution rules with varied lengths that are guaranteed to match."""
    num_rules = random.randint(min_rules, max_rules)
    rules = {}
    substrings = list(set(re.findall(r'(?=(.{1,4}))', input_str)))  # Find patterns of 1 to 4 characters
    
    while len(rules) < num_rules and substrings:
        old = random.choice(substrings)
        new_length = random.randint(1, 4)  # New pattern length between 1 and 4 characters
        new = ''.join(random.choices(string.ascii_letters + string.digits, k=new_length))
        if old != new and old not in rules and new not in rules.values():  # Ensure distinct rules
            rules[old] = new
        substrings.remove(old)  # Prevent duplicate rules on the same pattern
    
    return rules

def apply_rules_with_transitions(input_str, rules):
    """Apply rules and track each transformation as a transition without duplicates."""
    modified_str = input_str
    transitions = []
    seen_states = set()
    applied_rules = set()  # Track unique rule applications (src -> tgt)
    
    while modified_str and modified_str not in seen_states:  # Avoid infinite loops
        seen_states.add(modified_str)
        rule_applied = False
        for old, new in rules.items():
            if old in modified_str:
                modified_str = modified_str.replace(old, new, 1)  # Apply each rule once per step
                if (old, new) not in applied_rules:
                    transitions.append({"src": old, "tgt": new})
                    applied_rules.add((old, new))
                rule_applied = True
                break  # Apply one rule at a time and then check all rules again
        if not rule_applied:
            break  # No more applicable rules
    
    # Ensure multiple transitions occur before reaching the final empty state
    if len(transitions) >= 2 and modified_str != "":
        transitions.append({"src": modified_str, "tgt": ""})
    
    return modified_str, transitions

def generate_puzzles(num_puzzles=50, output_dir="puzzles"):
    """Generate multiple puzzles and save them as JSON files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i in range(num_puzzles):
        problem_id = f"{i:03}"
        initial_string = generate_simple_string()
        rules = generate_effective_rules(input_str=initial_string)
        final_string, transitions = apply_rules_with_transitions(initial_string, rules)
        
        puzzle = {
            "problem_id": problem_id,
            "initial_string": initial_string,  # Keep the original string as the initial_string
            "transitions": transitions
        }
        
        with open(os.path.join(output_dir, f"puzzle_{problem_id}.json"), "w") as f:
            json.dump(puzzle, f, indent=4)

# Generate 100 puzzles
generate_puzzles()
