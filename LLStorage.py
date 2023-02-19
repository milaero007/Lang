import sqlite3

table_word_creation = "CREATE TABLE words \
            ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                word VARCHAR(40) NOT NULL, \
                word_type INT NOT NULL, \
                creation DATETIME, \
                lastshow DATETIME, \
                show_nr INT DEFAULT 0, \
                error_nr INT DEFAULT 0, \
                score INT DEFAULT 0 \
            )"
table_translations_creation = "CREATE TABLE translations \
            ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                word VARCHAR(40) NOT NULL \
            )"
table_links_creation = "CREATE TABLE links \
            ( \
                id_word INT NOT NULL, \
                id_translation INT NOT NULL \
            )"
table_insertion_new_word = "INSERT INTO words(word, word_type, creation, show_nr, error_nr, score) \
    VALUES('{}', {}, datetime('now'), 0, 0, 0)"

table_update_word = "UPDATE words SET lastshow = datetime('now'), show_nr = {}, error_nr = {} WHERE id = {};"

table_remove_word_by_word = "DELETE FROM words WHERE word = '{}'"
table_remove_word_by_id = "DELETE FROM words WHERE id = '{}'"
table_remove_links_by_id_word = "DELETE FROM links WHERE id_word = '{}'"
table_remove_links_by_id_tr = "DELETE FROM links WHERE id_translation = '{}'"

table_insertion_new_translation = "INSERT INTO translations(word) VALUES('{}')"
table_remove_translation = "DELETE FROM translations WHERE id = '{}'"

table_update_existing_word = "UPDATE words SET word='{}', word_type='{}', lastshow = NULL,\
  show_nr=0, error_nr=0 WHERE id={}"

table_insert_new_links = "INSERT INTO links(id_word, id_translation)  VALUES({}, {})"

table_remove_links = "DELETE FROM links WHERE id_word = '{}' AND  id_translation = '{}'"

table_check_links = "SELECT * FROM links WHERE id_word = '{}' AND  id_translation = '{}'"

table_select_links = "SELECT * FROM translations WHERE  id IN (SELECT id_translation FROM links WHERE id_word = '{}')"

table_remove_all_links = "DELETE FROM links WHERE id_word = {}"

###  --- PLAYING ---
initial_play_rqst = "SELECT * FROM words WHERE lastshow IS NULL ORDER BY id LIMIT '{}';"
reset_all_stats_rqst = "UPDATE words SET lastshow=NULL, show_nr = 0, error_nr = 0, score = 0 WHERE True;"
reset_all_stats_rqst = "UPDATE words SET lastshow=NULL, show_nr = 0, error_nr = 0, score = 0 WHERE True;"

class SQLite:
    db_connection = []

    def __init__(self):
        self.db_connection = sqlite3.connect("ll.db")

    def isPasswordOK(self, password: str) -> bool:
        if password == "Tusik":
            return True
        return False

    def create_tables(self):
        self.db_connection.execute(table_word_creation)
        self.db_connection.execute(table_translations_creation)
        self.db_connection.execute(table_links_creation)

    def drop_tables(self):
        try:
            self.db_connection.execute("DROP TABLE words;")
        except Exception as e:
            print("Can't drop table words:", e)
            raise e
        try:
            self.db_connection.execute("DROP TABLE translations;")
        except Exception as e:
            print("Can't drop table translations 1")
            raise e
        try:
            self.db_connection.execute("DROP TABLE links;")
        except Exception as e:
            print("Can't drop table links 1")
            raise e

    def insert_new_word(self, word: str, word_type: int):
        rqst = table_insertion_new_word.format(word, word_type)
        print(rqst)
        self.db_connection.execute(rqst)
        self.db_connection.commit()

    def remove_word_by_word(self, word: str):
        rqst = table_remove_word_by_word.format(word)
        print(rqst)
        self.db_connection.execute(rqst)
        self.db_connection.commit()

    def remove_word_by_id(self, id: int):
        rqst = table_remove_word_by_id.format(id)
        print("Rqst1:", rqst)
        self.db_connection.execute(rqst)
        self.db_connection.commit()
        rqst = table_remove_links_by_id_word.format(id)
        print("Rqst2:", rqst)
        self.db_connection.execute(rqst)
        self.db_connection.commit()

    def insert_new_translation(self, word: str):
        rqst = table_insertion_new_translation.format(word)
        print(rqst)
        self.db_connection.execute(rqst)
        self.db_connection.commit()

    def remove_translation(self, id: int):
        rqst = table_remove_translation.format(id)
        print(rqst)
        self.db_connection.execute(rqst)
        self.db_connection.commit()
        rqst = table_remove_links_by_id_tr.format(id)
        self.db_connection.execute(rqst)
        self.db_connection.commit()



    def update_word(self, word: str, word_type: int, id: int):
        rqst = table_update_existing_word.format(word, word_type, id)
        print(rqst)
        self.db_connection.execute(rqst)
        self.db_connection.commit()

    def get_words(self, word="", like=False, limit=-1):
        cur = self.db_connection.cursor()
        limit_statement = ""
        if limit > 0:
            limit_statement = " LIMIT " + str(limit)
        if word == "":
            full_statement = "SELECT * FROM words ORDER by word ASC" + limit_statement
        elif like:
            full_statement = "SELECT * FROM words WHERE word LIKE '" + word + "%' ORDER by word ASC" + limit_statement
        else:
            full_statement = "SELECT * FROM words WHERE word='" + word + "' ORDER by word ASC" + limit_statement
        print("full_sql_statement: " + full_statement)
        cur.execute(full_statement)
        rows = cur.fetchall()
        return rows


    def is_word_present(self, word, word_type) -> bool:
        request = "SELECT * FROM words WHERE word = '{}' and word_type={};".format(word, word_type)
        cur = self.db_connection.cursor()
        cur.execute(request)
        rows = cur.fetchall()
        print("len(rows)=", len(rows))
        if len(rows) > 0:
            return True
        return False

    def get_translations(self, translation="", like=False, limit=-1):
        cur = self.db_connection.cursor()
        limit_statement = ""
        if limit > 0:
            limit_statement = " LIMIT " + str(limit)
        if translation == "":
            full_statement = "SELECT * FROM translations ORDER by word ASC" + limit_statement;
        elif like:
            full_statement = "SELECT * FROM translations WHERE word LIKE '" + translation + "%' ORDER by word ASC" + limit_statement
        else:
            full_statement = "SELECT * FROM translations WHERE word='" + translation + "' ORDER by word ASC" + limit_statement
        print("full_sql_statement: " + full_statement)
        cur.execute(full_statement)
        rows = cur.fetchall()
        return rows

    def is_translation_present(self, word) -> bool:
        rqst = "SELECT * FROM translations WHERE word = '{}';".format(word)
        cur = self.db_connection.cursor()
        cur.execute(rqst)
        rows = cur.fetchall()
        print("len(rows)=", len(rows))
        if len(rows) > 0:
            return True
        return False

#  LINKS
    def is_link_present(self, id_word: int, id_translation: int) -> bool:
        rqst = table_check_links.format(id_word, id_translation)
        cur = self.db_connection.cursor()
        cur.execute(rqst)
        rows = cur.fetchall()
        return len(rows) > 0

    def get_translations_4word(self, id_word: int) -> []:
        rqst = table_select_links.format(id_word)
        cur = self.db_connection.cursor()
        cur.execute(rqst)
        rows = cur.fetchall()
        return rows

    def add_link(self, id_word: int, id_translation: int) -> None:
        rqst = table_insert_new_links.format(id_word, id_translation)
        self.db_connection.execute(rqst)
        self.db_connection.commit()

    def remove_link(self, id_word: int, id_translation: int) -> None:
        rqst = table_remove_links.format(id_word, id_translation)
        self.db_connection.execute(rqst)
        self.db_connection.commit()

    def reset_all_stats(self) -> None:
        self.db_connection.execute(reset_all_stats_rqst)
        self.db_connection.commit()

