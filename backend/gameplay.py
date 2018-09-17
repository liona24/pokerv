import threading
import time

from pokergame import Game, player

import serialization as ser


class ReportingPlayer(player.PlayerBase):

    def __init__(self, name, initstack, sid, room, socket):
        player.PlayerBase.__init__(self, name, initstack)

        self.sid = sid
        self.room = room
        self.socket = socket

    def move(self, players, board, to_call):

        payload = {
            'board': ser.serialize_cards(board),
            'to_call': to_call,
            'players': ser.serialize_players(players, self)
        }

        self.socket.emit('move', payload, room=self.room.name)

        return player.PlayerBase.move(self, players, board, to_call)


class AiPlayer(ReportingPlayer):

    def __init__(self, name, initstack, sid, room, socket, *dummy):
        ReportingPlayer.__init__(self, name, initstack, sid, room, socket)

    def move(self, players, board, to_call):
        rv = ReportingPlayer.move(self, players, board, to_call)
        time.sleep(1)
        return rv


class HumanPlayer(ReportingPlayer):

    def __init__(self, name, initstack, sid, room, socket, event_storage):
        ReportingPlayer.__init__(self, name, initstack, sid, room, socket)

        self.event_storage = event_storage

    def move(self, players, board, to_call):

        event = threading.Event()
        event.data = {}
        self.event_storage[self.room.name][self.name] = event

        ReportingPlayer.move(self, players, board, to_call)

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
            self.stop_playing = None
            return 'ok', 200, 'Game will pause after this hand finished!'

        return 'err', 404, 'The game is not running!'

    def serialize_players(self):
        return ser.serialize_players(self.game.players,
                                     self.game.players,
                                     None)

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
