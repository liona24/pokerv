<template>
    <player-hud :player="player" :room="room" :board="board" :playing="playing" :pot="pot" :to-call="toCall" @playpause="playPause">
        <poker-table :players="players" :front="self" :pot="pot" />
    </player-hud>
</template>

<script>
import PlayerHud from './PlayerHud.vue'
import PokerTable from './PokerTable.vue'

import { joinRoom } from '../communication.js'
import { flash, handFinished } from '../EventBus.js'

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
            toCall: 0,
            players: [],
            playing: false
        }
    },
    computed: {
        player: function() {
            return (this.players[this.self] || {
                name: this.user,
                stack: 0,
                bet: 0,
                has_folded: false,
                action_required: false
            });
        }
    },
    created: function() {
        this.$socket.on('move', this.onMove);
        this.$socket.on('players changed', this.onPlayersChanged);
        this.$socket.on('hand finished', this.onHandFinished);

        joinRoom(this.$socket, this.room, this.user, 'human').then(
            (resp) => {
                if (resp.msg) {
                    flash(resp.status, resp.msg);
                }

                if (resp.status !== 'ok') {
                    this.$emit('leavegame');
                }
            }
        );
    },
    beforeDestroy: function() {
        this.$socket.off('move', this.onMove);
        this.$socket.off('players changed', this.onPlayersChanged);
        this.$socket.off('hand finished', this.onHandFinished);
    },
    methods: {
        playPause: function(e) {
            this.$socket.emit('playpause', { play: e.play, room: this.room },
                (resp) => {
                    if (resp.msg) {
                        flash(resp.status, resp.msg);
                    }
                    if (resp.status == 'ok') {
                        this.playing = e.play;
                    }
                }
            );
        },
        onMove: function(data) {
            console.log('onMove');
            console.log(JSON.stringify(data));

            this.pot = data.pot;
            this.board = data.board;
            this.toCall = data.to_call;

            this.players = data.players.reverse();

        },
        onPlayersChanged: function(data) {
            console.log('onJoin', data);

            // reverse because of some drawing logic 'flaw'
            this.players = data.players.reverse();
            this.self = this.players.findIndex(player => player.name === this.user);
        },
        onHandFinished: function(data) {
            console.log('onHandFinished');
            console.log(JSON.stringify(data));

            handFinished(data.hands_played, data.board, data.winners);
        }
    }
}
</script>

<style>

</style>
