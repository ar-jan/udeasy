import os
import pathlib
import sqlite3


PROJROOT = pathlib.Path(__file__).parents[1].resolve()
DBPATH = os.path.join(PROJROOT, 'translations.db')
conn = sqlite3.connect(DBPATH)
cur = conn.cursor()


def get_translation(sent_id):
    """ Takes a sentence_id as argument, and returns the corresponding translation
    :param sent_id: the sentence_id
    :return: string with the sentence translation
    """
    translation = cur.execute(
        ''' SELECT sentence_text_translation
        FROM sentences
        WHERE sentence_id = :sent_id;
        ''', {'sent_id': sent_id}
        ).fetchone()

    return translation
