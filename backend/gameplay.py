import threading
import time

from pokergame import Game, player
from deuces import Card


def serialize_card(card):
    suit_int = Card.get_suit_int(card)
    rank_int = Card.get_rank_int(card)

    s = Card.INT_SUIT_TO_CHAR_SUIT[suit_int]
    r = Card.STR_RANKS[rank_int]

    return s + r


def serialize_cards(cards):
    return list(map(serialize_card, cards))


def serialize_players(players, active_players, player_at_action):
    return [ {
        'name': p.name,
        'stack': p.stack,
        'bet': p.bet,
        'hand': serialize_cards(p.hand),
        'action_required': p == player_at_action,
        'folded': p not in active_players
    } for p in players ]


class ReportingPlayer(player.PlayerBase):

    def __init__(self, name, initstack, sid, room, socket):
        player.PlayerBase.__init__(self, name, initstack)

        self.sid = sid
        self.room = room
        self.socket = socket

    def move(self, players, board, to_call, pot):

        all_players = self.room.game.players
        payload = {
            'board': serialize_cards(board),
            'to_call': to_call,
            'pot': pot,
            'players': serialize_players(all_players, players, self),
        }

        self.socket.emit('move', payload, room=self.room.name)

        return player.PlayerBase.move(self, players, board, to_call, pot)


class AiPlayer(ReportingPlayer):

    def __init__(self, name, initstack, sid, room, socket, *dummy):
        ReportingPlayer.__init__(self, name, initstack, sid, room, socket)

    def move(self, players, board, to_call, pot):
        rv = ReportingPlayer.move(self, players, board, to_call, pot)
        time.sleep(1)
        return rv


class HumanPlayer(ReportingPlayer):

    def __init__(self, name, initstack, sid, room, socket, event_storage):
        ReportingPlayer.__init__(self, name, initstack, sid, room, socket)

        self.event_storage = event_storage

    def move(self, players, board, to_call, pot):

        event = threading.Event()
        event.data = {}
        self.event_storage[self.room.name][self.name] = event

        ReportingPlayer.move(self, players, board, to_call, pot)

        event.wait()
        return int(event.data['betsize'])


class Room(object):

    def __init__(self, name, max_size, initstack, blinds):
        self.name = name
        self.max_size = max_size
        self.initstack = initstack

        self.game = Game([], blinds)
        self.stop_playing = None

    def start_game(self, summary_hook):
        if len(self.game.players) > 1:
            if self.stop_playing is not None:
                return 'ok', 200, 'The game is already running!'

            self.stop_playing = self.game.play_async(None,
                                                     summary_hook=summary_hook)
            return 'ok', 200, 'The game started!'

        return 'err', 404, 'Congratz! You played against yourself and won!'

    def stop_game(self):
        if self.stop_playing is not None:
            self.stop_playing()
            return 'ok', 200, 'Game will pause after this hand finished!'

        return 'err', 404, 'The game is not running!'

    def serialize_players(self):
        return serialize_players(self.game.players, self.game.players, None)

    def join(self, player):

        if len(self.game.players) < self.max_size:
            if player.name not in map(lambda p: p.name, self.game.players):
                self.game.join(player, -1)

                return 'ok', 200, ''

            return 'err', 404, "A player with name '%s' already exists!"\
                % player.name

        return 'err', 404, 'The table is full!'

    def leave(self, player_name):

        for p in self.game.players:
            if getattr(p, 'name', None) == player_name:
                break
        else:
            return 'err', 404, "The player '%s' does not exist!"\
                % str(player_name)

        self.game.leave(p)
        return 'ok', 200, '%s left the game!' % player_name

    @property
    def isempty(self):
        return bool(len(self.game.players))
