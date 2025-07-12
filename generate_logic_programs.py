import openai
import os
import subprocess
import re

# -- Config --
PARENT_DIR = "logic_programs"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("Set your OPENAI_API_KEY as an environment variable.")

openai.api_key = OPENAI_API_KEY

def get_next_title_and_filename(folder, prog_title):
    os.makedirs(folder, exist_ok=True)
    files = [f for f in os.listdir(folder) if f.endswith('.py')]
    nums = [int(re.match(r"^(\d+)-", f).group(1)) for f in files if re.match(r"^(\d+)-", f)]
    next_num = max(nums) + 1 if nums else 1
    serial = f"{next_num:03d}"
    # Sanitize program title for filename
    clean_title = re.sub(r"[^A-Za-z0-9]", "", prog_title.replace(" ", ""))
    filename = f"{serial}-{clean_title}.py"
    return os.path.join(folder, filename), serial

def get_logic_problem():
    prompt = (
        "Pick a logic-based Python programming problem that tests understanding of Python, "
        "similar to those found on GeeksforGeeks, Leetcode, or Code Ninja. "
        "Return ONLY the problem title and a short description in one line, separated by a colon. "
        "For example: 'Bubble Sort: Implement the bubble sort algorithm on a list of integers.'"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.9,
    )
    return response.choices[0].message['content'].strip()

def generate_program(title, description, serial):
    prompt = (
        f"Write a complete Python program for the following logic-based problem.\n"
        f"Title: {serial}-{title}\nDescription: {description}\n"
        "At the top, include the title as a comment, followed by the problem description as comments. "
        "Then write the full code with comments. No explanations, only the program with comments."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()

def git_add_commit_push(filepath, commit_msg):
    subprocess.run(["git", "add", filepath], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    # 1. Get a logic-based problem
    logic_line = get_logic_problem()
    if ":" in logic_line:
        title, desc = [x.strip() for x in logic_line.split(":", 1)]
    else:
        title = logic_line.strip()
        desc = ""

    # 2. Get numbered filename and serial
    filepath, serial = get_next_title_and_filename(PARENT_DIR, title)

    # 3. Generate code
    code = generate_program(title, desc, serial)

    # 4. Save to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    # 5. Git add/commit/push
    commit_message = f"Add logic-based program: {serial}-{title}"
    git_add_commit_push(filepath, commit_message)

if __name__ == "__main__":
    main()