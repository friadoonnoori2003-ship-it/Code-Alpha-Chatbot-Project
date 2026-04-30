"""
╔══════════════════════════════════════════════════════════╗
║          BASIC CHATBOT — CodeAlpha Internship            ║
║                      Task 4                              ║
╚══════════════════════════════════════════════════════════╝
"""

import random
import time


# ──────────────────────────────────────────────────────────
# Response rules: each key is a tuple of trigger keywords;
# the value is a list of possible replies (chosen randomly).
# ──────────────────────────────────────────────────────────
RULES: list[tuple[tuple[str, ...], list[str]]] = [
    # Greetings
    (("hello", "hi", "hey", "howdy", "sup", "greetings"),
     ["Hello there! 👋 How can I help you today?",
      "Hey! Great to see you. What's on your mind?",
      "Hi! I'm Alpha, your friendly CodeAlpha bot. How can I assist?"]),

    # How are you
    (("how are you", "how r u", "how do you do", "how's it going",
      "hows it going", "what's up", "whats up", "how have you been"),
     ["I'm doing great, thanks for asking! 😊 How about you?",
      "All systems running smoothly! Hope you're having a wonderful day.",
      "Fantastic as always! What can I do for you?"]),

    # User is fine / good
    (("i'm good", "im good", "i am good", "i'm fine", "im fine",
      "good", "great", "awesome", "fantastic", "not bad"),
     ["That's wonderful to hear! 🎉",
      "Glad to know you're doing well!",
      "Awesome! Let's make it an even better day. How can I help?"]),

    # User is sad / bad
    (("i'm sad", "im sad", "not good", "i'm bad", "im bad",
      "not well", "terrible", "awful", "depressed", "lonely"),
     ["I'm sorry to hear that. 😔 Remember, tough times don't last forever!",
      "Sending virtual hugs your way. 🤗 Is there anything I can do to help?",
      "I'm here for you! Things will get better. Would you like to talk?"]),

    # Name queries
    (("what is your name", "what's your name", "whats your name",
      "who are you", "your name"),
     ["I'm **Alpha** 🤖, the CodeAlpha internship chatbot!",
      "You can call me Alpha — your go-to CodeAlpha assistant.",
      "I'm Alpha, built with Python for the CodeAlpha internship. Nice to meet you!"]),

    # What can you do
    (("what can you do", "help", "capabilities", "features",
      "what do you know", "abilities"),
     ["I can chat with you, answer basic questions, tell jokes, and share fun facts! 😄",
      "I'm a friendly rule-based bot — ask me how I am, for a joke, or a fun fact!",
      "Try asking me: a joke, a fun fact, the time, or just chat with me!"]),

    # Jokes
    (("joke", "tell me a joke", "funny", "make me laugh", "humor"),
     ["Why do programmers prefer dark mode? Because light attracts bugs! 🐛😂",
      "Why was the Python developer always calm? Because they never lost their 'cool'! 🐍😄",
      "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads. 🍫😂",
      "Why do Java developers wear glasses? Because they don't C#! 😂"]),

    # Fun facts
    (("fun fact", "fact", "interesting", "did you know", "tell me something"),
     ["🌍 Fun fact: There are more possible iterations of a game of chess than atoms in the observable universe!",
      "🐙 Fun fact: Octopuses have three hearts and blue blood!",
      "🐍 Fun fact: Python was named after 'Monty Python's Flying Circus', not the snake!",
      "💻 Fun fact: The first computer bug was an actual bug — a moth found in a Harvard Mark II computer in 1947!"]),

    # Time
    (("time", "what time", "current time", "what's the time"),
     [lambda: f"⏰ The current time is {time.strftime('%H:%M:%S')}."]),

    # Date
    (("date", "what date", "today's date", "what day"),
     [lambda: f"📅 Today is {time.strftime('%A, %B %d, %Y')}."]),

    # Python / coding
    (("python", "programming", "code", "coding", "developer"),
     ["Python is an amazing language! 🐍 Are you learning it for the CodeAlpha internship?",
      "Coding is a superpower! Keep building cool things with Python. 💻",
      "Python is great for automation, data science, web development and more!"]),

    # CodeAlpha
    (("codealpha", "code alpha", "internship", "company"),
     ["CodeAlpha is a leading software development company. Great choice for an internship! 🚀",
      "This chatbot was built as part of the CodeAlpha Python internship programme! 🎓",
      "CodeAlpha offers fantastic internship experiences in Python, AI, and more!"]),

    # Thank you
    (("thank", "thanks", "thank you", "thx", "ty"),
     ["You're very welcome! 😊",
      "Happy to help! Anytime.",
      "No problem at all! 🙌"]),

    # Goodbye
    (("bye", "goodbye", "see you", "see ya", "quit", "exit",
      "cya", "later", "farewell", "take care"),
     ["Goodbye! Have a wonderful day! 👋",
      "See you later! Keep coding! 🐍",
      "Farewell! It was a pleasure chatting with you! 😊"]),
]

GOODBYE_TRIGGERS = {"bye", "goodbye", "see you", "see ya", "quit",
                    "exit", "cya", "later", "farewell", "take care"}

FALLBACK_RESPONSES = [
    "Hmm, I'm not sure I understand. Could you rephrase that? 🤔",
    "Interesting! I'm still learning. Can you ask me something else?",
    "I didn't quite catch that. Try asking for a joke or a fun fact! 😄",
    "That's a bit beyond my knowledge right now. Ask me something simpler!",
]


def find_response(user_input: str) -> tuple[str, bool]:
    """
    Match *user_input* against RULES and return (reply, is_goodbye).
    Matching is case-insensitive and checks if any trigger keyword is
    contained in the user input.
    """
    text = user_input.lower().strip()
    is_goodbye = any(trigger in text for trigger in GOODBYE_TRIGGERS)

    for keywords, replies in RULES:
        if any(kw in text for kw in keywords):
            chosen = random.choice(replies)
            # Support lambda replies (e.g., for time/date)
            return (chosen() if callable(chosen) else chosen), is_goodbye

    return random.choice(FALLBACK_RESPONSES), is_goodbye


def typing_effect(text: str, delay: float = 0.02) -> None:
    """Print text with a subtle typing effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def main() -> None:
    print("\n" + "=" * 60)
    print("   🤖  ALPHA — CodeAlpha Internship Chatbot")
    print("=" * 60)
    print("   Type a message to chat. Type 'bye' to exit.")
    print("=" * 60 + "\n")

    # Greet the user
    time.sleep(0.3)
    typing_effect("Alpha: Hello! I'm Alpha, your CodeAlpha assistant. 😊")
    typing_effect("Alpha: How can I help you today?\n")

    while True:
        try:
            user_input = input("You  : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAlpha: Caught a keyboard interrupt — Goodbye! 👋\n")
            break

        if not user_input:
            print("Alpha: (Please type something — I'm listening!)\n")
            continue

        response, is_goodbye = find_response(user_input)

        time.sleep(0.4)          # simulate "thinking"
        typing_effect(f"Alpha: {response}\n")

        if is_goodbye:
            break


if __name__ == "__main__":
    main()
