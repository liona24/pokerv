<template>
    <player-hud :room="room" :board="board" :hand="hand" :playing="playing" @playpause="playPause">
        <poker-table :players="players" :front="self" :pot="pot" />
    </player-hud>
</template>

<script>
import PlayerHud from './PlayerHud.vue'
import PokerTable from './PokerTable.vue'

import { joinRoom } from '../communication.js'
import { flash } from '../EventBus.js'

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
            pot: 0,
            self: 0,
            players: [],
            playing: false
        }
    },
    computed: {
        hand: function() {
            return (this.players[this.self] || { hand: [] }).hand;
        }
    },
    created: function() {
        this.$socket.on('move', this.onMove);
        this.$socket.on('join', this.onJoin);

        joinRoom(this.$socket, this.room, this.user, 'human').then(
            (status, code, msg) => {
                if (msg) {
                    flash(status, msg);
                }

                // TODO leave room on error
            }
        );
    },
    beforeDestroy: function() {
        this.$socket.off('move', this.onMove);
        this.$socket.off('join', this.onJoin);
    },
    methods: {
        playPause: function(e) {
            this.$socket.emit('playpause', { play: e.play, room: this.room },
                (resp) => {
                    if (resp.msg) {
                        flash(resp.status, resp.msg);
                    }
                    if (resp.status == 'ok') {
                        this.playing = !e.play;
                    }
                }
            );
        },
        onMove: function(data) {
            console.log('onMove');
            console.log(JSON.stringify(data));

            this.pot = data.pot;
            this.board = data.board;

            this.players = data.players;

        },
        onJoin: function(data) {
            console.log('onJoin', data);

            this.players = data.players;
            this.self = this.players.findIndex(player => player.name === this.user);
        }
    }
}
</script>

<style>

</style>
