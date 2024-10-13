import sqlite3


class Database:
    EXAMPLES_SEPARATOR = '@@@'

    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY,
                word TEXT UNIQUE,
                definition TEXT,
                examples TEXT
            )
        ''')
        self.connection.commit()
        self.connection.close()

    def connect(self):
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()

    def save_word(self, word, definition, examples=[]):
        if type(examples) is list:
            examples = self.EXAMPLES_SEPARATOR.join(examples)
        self.connect()
        self.cursor.execute(
            'INSERT OR IGNORE INTO words (word, definition, examples) VALUES (?, ?, ?)', (word, definition, examples))
        self.connection.commit()
        self.connection.close()

    def list_words(self):
        self.connect()
        self.cursor.execute('SELECT word, definition, examples FROM words')
        words = self.cursor.fetchall()
        self.connection.close()
        processed_words = []
        for word, definition, examples in words:
            examples_list = examples.split(
                self.EXAMPLES_SEPARATOR) if examples else []
            processed_words.append((word, definition, examples_list))
        return processed_words

    def get_by_word(self, word_to_search):
        self.connect()
        self.cursor.execute(
            'SELECT word, definition, examples FROM words WHERE word=?', (word_to_search,))
        word = self.cursor.fetchone()
        self.connection.close()
        return word

    def get_random_word(self):
        self.connect()
        self.cursor.execute(
            'SELECT word, definition, examples FROM words ORDER BY RANDOM() LIMIT 1')
        word = self.cursor.fetchone()
        self.connection.close()
        return word
