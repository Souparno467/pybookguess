from flask import Flask, render_template, request, redirect, url_for, g
import random
import google.generativeai as genai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API key from .env
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Please check your .env file.")

genai.configure(api_key=api_key)

# List of books (classics & bestsellers)
BOOKS = [
    "Pride and Prejudice", "1984", "To Kill a Mockingbird", "The Great Gatsby",
    "Moby-Dick", "The Catcher in the Rye", "The Hobbit", "Harry Potter and the Sorcerer's Stone",
    "The Lord of the Rings", "War and Peace", "Notes from Underground", "Metamorphosis",
    "David Copperfield", "The Bell Jar", "Macbeth", "King Lear", "Symposium", "Oliver Twist",
    "Nausea", "Hamlet", "Othello", "White Nights", "The Outsider", "A Happy Death",
    "Man's Search for Meaning", "Meditations", "The Myth of Sisyphus", "Beyond Good and Evil",
    "Ulysses", "Wuthering Heights", "The Picture of Dorian Gray", "Great Expectations",
    "Letters to Milena", "The Communist Manifesto", "Crime and Punishment",
    "Absolute Spirit", "No Longer Human", "Don Quixote"
]

# Encouraging messages
COMPLIMENTS = [
    "🎉 Amazing! You truly have the mind of a literary genius!",
    "🌟 Brilliant! You could be a book critic!",
    "📚 Fantastic! You really know your books!",
    "🔥 Outstanding! A true bibliophile at heart!",
    "💡 Genius! That was an impressive guess!"
]

def get_hint(book_name):
    """Generates a hint for a given book using Google Generative AI."""
    prompt = f"Provide a cryptic but helpful hint for the book '{book_name}'."
    
    try:
        model = genai.GenerativeModel("gemini-pro")  # Use Gemini model
        response = model.generate_content(prompt)  # Correct API call

        return response.text.strip() if response.text else "No hint available."
    except Exception as e:
        return f"Error generating hint: {str(e)}"

@app.before_request
def before_request():
    """Runs before each request to initialize a book and hint."""
    g.book = random.choice(BOOKS)
    g.hint = get_hint(g.book)
    g.message = ""
    g.correct = False

@app.route('/')
def index():
    return render_template('index.html', hint=g.hint, message=g.message, correct=g.correct)

@app.route('/guess', methods=['POST'])
def guess():
    user_guess = request.form.get('guess', '').strip()
    if user_guess.lower() == g.book.lower():
        g.message = random.choice(COMPLIMENTS)
        g.correct = True
    else:
        g.message = "❌ Incorrect. Try again."
        g.correct = False
    return render_template('index.html', hint=g.hint, message=g.message, correct=g.correct)

@app.route('/restart')
def restart():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
