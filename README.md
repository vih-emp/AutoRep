# Logic Program Auto-Generator

## Overview

This project is an automated code generation system that creates logic-based Python programs using AI (OpenAI's GPT API) and manages their versioning using Git. The programs are inspired by classic problem types seen on platforms like GeeksforGeeks, Leetcode, and Code Ninja, but are **originally generated** and not direct copies from those sources.

All generated programs are saved in the `logic_programs/` directory, with clear, descriptive filenames (e.g., `001-BubbleSort.py`). The script ensures each file has a unique serial number and an appropriate title that reflects the core logic topic or algorithm implemented.

## What This Project Does

- **Automatically generates logic-based Python programs** using AI, with well-structured code and comments.
- **Saves each program in a unique, numbered file** under `logic_programs/`, titled with the serial number and main topic/algorithm.
- **Automates Git version control** by adding, committing, and pushing each new program to the repository, ensuring reproducibility and traceability.
- **Ensures all generated content is original** and does not copy or republish any proprietary material or verbatim problem statements from third-party platforms.

## My Statement

I created this project to:
- **Practice and reinforce Python fundamentals** by generating a wide variety of logic-based problems and solutions.
- **Build a personal library of example code** for learning, reference, and interview preparation.
- **Demonstrate automation skills** in code generation, file management, and version control.

All programs in this repository are **original and AI-generated**. They are not copied from GeeksforGeeks, Leetcode, Code Ninja, or any other third-party platform. The project does not aim to republish or distribute any proprietary or copyrighted material. Any resemblance of problem statements or solutions to those found elsewhere is purely coincidental and a result of common algorithmic practices in computer science education.

## Usage

1. **Set your OpenAI API key** as the `OPENAI_API_KEY` environment variable.
2. **Run the main script** in your terminal:
   ```sh
   python generate_logic_programs.py
   ```
3. **Each run produces a new, original program file** in the `logic_programs/` folder, and automatically commits and pushes it to the repo.

## Legal and Ethical Guidelines

- All content is **AI-generated and original**.
- No direct copying of third-party platform content occurs.
- This project is for **educational and personal development** purposes. If you wish to use the generated programs beyond this context, please ensure compliance with all relevant laws and platform terms of service.

## Contact

If you have questions or concerns about this project or its content, please open an issue or contact me directly.

```# AutoRep
