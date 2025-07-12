import os
import openai
import time
import json
import subprocess

# Set up the OpenAI client with your API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HISTORY_FILE = "logic_programs_history.json"
PROGRAM_DIR = "logic_programs"
TIMESTAMP_FILE = "last_generated_timestamp.txt"

def wait_if_needed():
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            last_time = float(f.read())
        now = time.time()
        elapsed = now - last_time
        if elapsed < 600:
            wait_time = int(600 - elapsed)
            print(f"Waiting {wait_time} seconds before generating next program...")
            time.sleep(wait_time)

def update_timestamp():
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(str(time.time()))

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_next_number():
    if not os.path.exists(PROGRAM_DIR):
        os.makedirs(PROGRAM_DIR)
        return 1
    files = [f for f in os.listdir(PROGRAM_DIR) if f.endswith(".py")]
    numbers = []
    for f in files:
        try:
            n = int(f.split('-')[0])
            numbers.append(n)
        except Exception:
            continue
    return max(numbers, default=0) + 1

def generate_unique_problem(history):
    prompt = (
        "Generate a unique, original, intermediate-to-advanced level logic-based Python programming problem. "
        "It should NOT be a basic beginner task (like Fibonacci, factorial, palindrome, prime check, etc.), "
        "and it should not repeat any of these previous problems:\n"
        + "\n".join(f"- {h['title']}" for h in history)
        + "\n\nProvide ONLY the problem title and a 1-2 sentence description."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.7,
    )
    content = response.choices[0].message.content.strip()
    # Parse title and description
    if "\n" in content:
        title, description = content.split("\n", 1)
        title = title.strip("- ").strip()
        description = description.strip()
    else:
        title = content
        description = ""
    return title, description

def generate_solution(problem_title, problem_description):
    prompt = (
        f"Write a complete, well-commented Python solution for the following programming problem.\n\n"
        f"Title: {problem_title}\nDescription: {problem_description}\n\n"
        f"Include comments explaining your logic."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def save_program_file(number, title, description, solution):
    safe_title = "".join(c if c.isalnum() else "" for c in title.replace(" ", ""))
    filename = f"{number:03d}-{safe_title[:25]}.py"
    path = os.path.join(PROGRAM_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n")
        f.write(f"# {description}\n\n")
        f.write(solution)
    return path

def git_commit_and_push(filepath, message):
    try:
        subprocess.run(["git", "add", filepath], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
    except Exception as e:
        print(f"Git commit/push failed: {e}")

def main():
    wait_if_needed()
    history = load_history()
    number = get_next_number()
    problem_title, problem_description = generate_unique_problem(history)
    solution = generate_solution(problem_title, problem_description)
    filepath = save_program_file(number, problem_title, problem_description, solution)
    # Update history
    history.append({"number": number, "title": problem_title, "description": problem_description})
    save_history(history)
    # Git commit & push
    git_commit_and_push(filepath, f"Add program {number:03d}: {problem_title}")
    update_timestamp()
    print(f"Generated and saved: {filepath}")

if __name__ == "__main__":
    main()