import hug
import plyvel
import arrow
from datetime import datetime


def database(user_id):
    '''Returns the level db unique to the given user_name'''
    return plyvel.DB('/clippify/users/{user_id}'.format(user_id=user_id), create_if_missing=True)


@hug.get()
def get_notes(user:database):
    '''Returns all notes for the specified user'''
    return {date: note for date, note in user}


@hug.post(('/{user}/note/', '/{user}/note/{timestamp}'))
def save_note(user:database, note, timestamp:arrow.get=None):
    '''Saves a note in the specified user database, or updates an existing one with a set timestamp'''
    timestamp = timestamp or arrow.get()
    user.put(bytes(timestamp), bytes(note))
    return timestamp
