#!/usr/bin/env python3

import nltk
from nltk.corpus import wordnet as wn
import argparse
import os
import sqlite3
import curses

DB_FILE = os.path.expanduser('~/.telesm.db')
EXAMPLES_SEPARATOR = '@@@'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            word TEXT UNIQUE,
            definition TEXT,
            examples TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_word(word, definition, examples=[]):
    if type(examples) is list:
        examples = EXAMPLES_SEPARATOR.join(examples)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO words (word, definition, examples) VALUES (?, ?, ?)', (word, definition, examples))
    conn.commit()
    conn.close()

def list_words():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT word, definition, examples FROM words')
    words = cursor.fetchall()
    conn.close()
    return words

def get_random_word():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT word, definition, examples FROM words ORDER BY RANDOM() LIMIT 1')
    word = cursor.fetchone()
    conn.close()
    return word

def format_word_with_definition_and_examples(word, definition, examples=[]):
    if examples:
        if type(examples) is str:
            examples = examples.split(EXAMPLES_SEPARATOR)
        formatted_examples = "\n".join(f"\t⁃ {example}" for example in examples)
        examples_text = f"\nExamples:\n{formatted_examples}"
    else:
        examples_text = ""

    return f"{word}:\n\t‣ {definition}{examples_text}"

def display_words_with_navigation(saved_words):
    def navigate_words(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        current_index = 0
        total = len(saved_words)

        while True:
            stdscr.clear()
            word, definition, examples = saved_words[current_index]
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(0, 0, f"{word}:")
            stdscr.addstr(1, 4, f"{definition[:curses.COLS - 1]}")
            if examples:
                stdscr.addstr(2, 0, "Examples:")
                for i, example in enumerate(examples.split(EXAMPLES_SEPARATOR)):
                    stdscr.addstr(3+i, 4, f"- {example}")
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(curses.LINES - 3, 0, f"({current_index+1}/{total})")
            stdscr.addstr(curses.LINES - 2, 0, "Press 'J' to move down, 'K' to move up, 'Q' to quit.")
            stdscr.attroff(curses.color_pair(2))
            stdscr.refresh()

            key = stdscr.getch()

            if key == ord('j') and current_index < len(saved_words) - 1:
                current_index += 1
            elif key == ord('k') and current_index > 0:
                current_index -= 1
            elif key == ord('q'):
                break
    curses.wrapper(navigate_words)

def get_word_definition(word):
    synsets = wn.synsets(word)

    if not synsets:
        return f"No definition found for '{word}'"
    
    definition = synsets[0].definition()
    examples = synsets[0].examples()
    return definition, examples
    

def parse_args():
    parser = argparse.ArgumentParser(description='Get the definition of a word')
    parser.add_argument('word', nargs='?', type=str, help='The word to define')
    parser.add_argument('--list', action='store_true', help='List all saved words')
    parser.add_argument('--navigate', action='store_true', help='Navigate through saved words')
    parser.add_argument('--no-save', action='store_true', help='Do not save the searched word in the database')
    parser.add_argument('--random', action='store_true', help='Display a random word from the database')
    return parser.parse_args()

def main():
    nltk.download('wordnet', quiet=True)
    args = parse_args()
    if args.list:
        saved_words = list_words()
        if not saved_words:
            print("No words saved yet.")
            exit(0)
        else:
            if args.navigate:
                display_words_with_navigation(saved_words)
            else:
                for word, definition, examples in saved_words:
                    print(format_word_with_definition_and_examples(word, definition, examples))
                    print("---")
    elif args.word:
        definition, examples = get_word_definition(args.word.strip().lower())
        print(format_word_with_definition_and_examples(args.word, definition, examples))
        if not args.no_save:
            save_word(args.word, definition, examples)
    elif args.random:
        random_word = get_random_word()
        if not random_word:
            print("No word could be found in the database.")
            exit(0)
        print(format_word_with_definition_and_examples(random_word[0], random_word[1], random_word[2]))

if __name__ == "__main__":
    init_db()
    main()