import os

def is_problem_already_solved(slug):
    return os.path.exists(f"solutions/{slug}.py")
