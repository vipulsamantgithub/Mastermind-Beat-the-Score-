import random
import time
import sqlite3

def generate_number():
    digits = list(range(10))
    random.shuffle(digits)
    return ''.join(map(str, digits[:4]))

def evaluate_guess(secret, guess):
    feedback = []
    for i in range(4):
        if guess[i] == secret[i]:
            feedback.append('+')
        elif guess[i] in secret:
            feedback.append('-')
        else:
            feedback.append('*')
    return ''.join(feedback)

def save_score(name, attempts, time_taken):
    conn = sqlite3.connect("C:/Users/SamantVi/OneDrive - Unisys/Desktop/Py/Chapter 14 -Project-3/game_scores.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            attempts INTEGER,
            time_taken REAL
        )
    """)
    cursor.execute("INSERT INTO scores (name, attempts, time_taken) VALUES (?, ?, ?)",
                   (name, attempts, time_taken))
    conn.commit()
    conn.close()

def get_best_score():
    conn = sqlite3.connect("C:/Users/SamantVi/OneDrive - Unisys/Desktop/Py/Chapter 14 -Project-3/game_scores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, attempts, time_taken FROM scores ORDER BY (attempts + time_taken) ASC LIMIT 1")
    best = cursor.fetchone()
    conn.close()
    return best

def show_all_scores():
    print("******* Leader Board *******")
    c=sqlite3.connect("C:/Users/SamantVi/OneDrive - Unisys/Desktop/Py/Chapter 14 -Project-3/game_scores.db")
    cur=c.cursor()
    cur.execute("Select * from scores")
    for row in cur:
        print(row)
    c.close()

def play_game():
    print("Welcome to the Guessing Number Game!")
    name = input("Enter your name: ")
    secret_number = generate_number()
    attempts = 0
    start_time = time.time()
    
    while True:
        guess = input("Enter a 4-digit number (no duplicate digits): ")
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
            print("Invalid input. Ensure 4 unique digits.")
            continue
        
        attempts += 1
        feedback = evaluate_guess(secret_number, guess)
        print("Feedback:", feedback)
        
        if feedback == "++++":
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print(f"Congratulations {name}! You guessed the number in {attempts} attempts and {time_taken} seconds.")
            save_score(name, attempts, time_taken)
            best_score = get_best_score()
            if best_score:
                print(f"Best Score: {best_score[0]} - {best_score[1]} attempts, {best_score[2]} seconds")
            show_all_scores()
            break

if __name__ == "__main__":
    play_game()
