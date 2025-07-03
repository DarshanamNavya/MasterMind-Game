from flask import Flask, render_template, request
import random

app = Flask(__name__)
colors = ["Red", "Green", "Yellow", "Blue", "Purple", "Orange"]
code_length = 4
max_attempts = 10

# Global game state
secret_code = random.choices(colors, k=code_length)
attempts = []

@app.route("/", methods=["GET", "POST"])
def index():
    global secret_code, attempts
    message = ""
    effect = ""
    if request.method == "POST":
        guess = request.form.get("guess").split()

        if len(guess) != code_length or not all(color.capitalize() in colors for color in guess):
            message = "Invalid guess! Pick exactly 4 valid colors."
        else:
            correct_positions = sum(g == c for g, c in zip(guess, secret_code))
            correct_colors = sum(min(guess.count(c), secret_code.count(c)) for c in set(secret_code))
            attempts.append({
                "guess": guess,
                "correct_positions": correct_positions,
                "wrong_positions": correct_colors - correct_positions
            })

            if correct_positions == code_length:
                message = "🎉 You cracked the code!"
                effect = "win"
            elif len(attempts) >= max_attempts:
                message = f"Game Over! The correct code was: {' '.join(secret_code)}"
                effect = "fail"

    remaining = max_attempts - len(attempts)

    if effect in ["win", "fail"]:
        final_code = secret_code.copy()
        secret_code = random.choices(colors, k=code_length)
        attempts = []
    else:
        final_code = None

    return render_template("index.html", colors=colors, attempts=attempts, message=message,
                           remaining=remaining, max_attempts=max_attempts, effect=effect, final_code=final_code)
