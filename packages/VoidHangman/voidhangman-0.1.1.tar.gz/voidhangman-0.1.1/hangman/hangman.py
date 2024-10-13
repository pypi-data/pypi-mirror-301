import random

WORD_LIST = ["boat", "disk", "code", "frog", "loop", "game", "best", "word"]

class Hangman:
    def __init__(self):
        self.word = random.choice(WORD_LIST)
        self.guesses = []
        self.max_attempts = 6
        self.attempts_left = self.max_attempts

    def guess(self, letter):
        if letter in self.guesses:
            return "You already guessed that letter."
        self.guesses.append(letter)

        if letter not in self.word:
            self.attempts_left -= 1
            return "Incorrect guess."
        return "Correct guess!"

    def get_display_word(self):
        return "".join([letter if letter in self.guesses else "_" for letter in self.word])

    def is_game_over(self):
        return self.attempts_left <= 0 or self.is_word_guessed()

    def is_word_guessed(self):
        return all(letter in self.guesses for letter in self.word)

    def get_attempts_left(self):
        return self.attempts_left

    def get_hangman_visual(self):
        stages = [
            "```\n  +---+\n      |\n      |\n      |\n      |\n      |\n=========\n```",  # 6 attempts left
            "```\n  +---+\n  O   |\n      |\n      |\n      |\n      |\n=========\n```",  # 5 attempts left
            "```\n  +---+\n  O   |\n  |   |\n      |\n      |\n      |\n=========\n```",  # 4 attempts left
            "```\n  +---+\n  O   |\n /|   |\n      |\n      |\n      |\n=========\n```",  # 3 attempts left
            "```\n  +---+\n  O   |\n /|\\  |\n      |\n      |\n      |\n=========\n```",  # 2 attempts left
            "```\n  +---+\n  O   |\n /|\\  |\n /    |\n      |\n      |\n=========\n```",  # 1 attempt left
            "```\n  +---+\n  O   |\n /|\\  |\n / \\  |\n      |\n      |\n=========\n```",  # 0 attempts left
        ]
        return stages[self.max_attempts - self.attempts_left]
