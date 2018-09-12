<template>
    <player-hud :board="board" :hand="hand" :playing="playing" @playpause="playPause">
        <poker-table :players="players" :fronti="self" :pot="pot"/>
    </player-hud>
</template>

<script>
import PlayerHud from './PlayerHud.vue'
import PokerTable from './PokerTable.vue'

import { joinRoom } from '../communication.js'

/*
                {
                    name: 'Player3',
                    stack: 10,
                    bet: 10,
                    itsTurn: true
                },
                */

export default {
    name: 'Game',
    components: {
        PlayerHud,
        PokerTable
    },
    props: {
        user: String,
        room: String
    },
    data: function() {
        return {
            board: [],
            hand: [],
            pot: 0,
            self: 0,
            players: [],
            playing: false
        }
    },
    created: function() {
        joinRoom(this.$socket, this.room, this.user, 'human').then(
            (status, code, msg) => {
                if (msg) {
                    flash(status, msg);
                }
            }
        );
    },
    methods: {
        playPause: function(e) {
            this.$socket.emit('playpause', { play: e.play, room: this.room },
                (status, code, msg) => {
                    if (msg) {
                        flash(status, msg);
                    }
                    if (status == 'ok') {
                        this.playing = !e.play;
                    }
                }
            );
        }
    },
    socket: {
        move: function(data) {
            console.log(data);
        },
        join: function(data) {
            this.players = data.players;
        }
    }
}
</script>

<style>

</style>
