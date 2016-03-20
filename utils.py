import logging
from google.appengine.ext import ndb
import endpoints

def get_by_urlsafe(urlsafe, model):
    """Returns an ndb.Model entity that the urlsafe key points to. Checks
        that the type of entity returned is of the correct kind. Raises an
        error if the key String is malformed or the entity is of the incorrect
        kind
    Args:
        urlsafe: A urlsafe key string
        model: The expected entity kind
    Returns:
        The entity that the urlsafe Key string points to or None if no entity
        exists.
    Raises:
        ValueError:"""
    try:
        key = ndb.Key(urlsafe=urlsafe)
    except TypeError:
        raise endpoints.BadRequestException('Invalid Key')
    except Exception, e:
        if e.__class__.__name__ == 'ProtocolBufferDecodeError':
            raise endpoints.BadRequestException('Invalid Key')
        else:
            raise

    entity = key.get()
    if not entity:
        return None
    if not isinstance(entity, model):
        raise ValueError('Incorrect Kind')
    return entity


def check_winner(game):
    """Check the board. If there is a winner, return the symbol of the winner"""
    # Check points
    if game.user_o.points > game.user_x.points:
        return game.user_o
    else:
        return game.user_x

def check_solutions(game):
    """Return true if the board is full"""
    return len(game.all_solutions)<1

def check_usermove(user_move, game):
    """Return true if move is valid"""
    return user_move in game.all_solutions

def points_for_valid_solution(user_move):
    """gets the points for the correct word"""
    word = user_move[0]
    if len(word) >= 8:
        return 11
    elif len(word) >= 7:
        return 5
    elif len(word) >= 6:
        return 3
    elif len(word) >= 5:
        return 2
    else:
        return 1
    return 0

def stringToTuple(string):
    """will attempt to convert 
    string into python format.
    Assumes python tuple format
    is in proper syntax, 
    else throws error"""
    try:
        return eval(string)
    except Exception:
        raise endpoints.BadRequestException('Tuple not in correct format ((1, 2), (3, 4))')


if __name__ == '__main__':
    print stringToTuple("((1, 2), (3, 4))")