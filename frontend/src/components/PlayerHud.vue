<template>
    <div name="player-hud">
        <div class="top-panel">
            <div class="float-right">
                <input type="button" value="Leave" @click="leave">

                <add-ai-menu v-if="showAiMenu" @close="showAiMenu = false" :room="room" />
                <input v-else type="button" value="Add AI" @click="addAi">
            </div>
            <div class="float-left">
                <input type="button" :value="playing ? 'Pause' : 'Start'" @click="playPause">
            </div>
        </div>
        <div class="card-panel board">
            <card v-for="(c, i) in board" :key="'boardcard-' + i" :ident="c"/>
        </div>
        <slot></slot>
        <div class="card-panel hand">
            <card v-for="(c, i) in player.hand" :key="'handcard-' + i" :ident="c"/>
        </div>
        <div class="bet-panel">
            <input type="number" v-model="betsize" name="betsize" :disabled="!player.action_required">
            <input type="button" value="Bet" @click="bet" :disabled="!player.action_required">
            <input type="button" value="Call" @click="call" :disabled="!player.action_required">
            <input type="button" value="Fold" @click="fold" :disabled="!player.action_required">
        </div>
    </div>
</template>

<script>
import Card from './Card.vue'
import AddAiMenu from './AddAiMenu.vue'

import { flash } from '../EventBus.js'
import { leaveRoom } from '../communication.js'

export default {
    name: 'PlayerHud',
    components: {
        Card,
        AddAiMenu
    },
    props: {
        board: Array,
        playing: Boolean,
        pot: Number,
        room: String,
        player: Object,
        toCall: Number
    },
    data: function() {
        return {
            betsize: 0,
            showAiMenu: false
        };
    },
    methods: {
        bet: function(e) {
            if (this.betsize > this.player.stack) {
                this.betsize = this.player.stack;
            }

            if (this.betsize < this.toCall) {
                flash('err', 'You have to bet at least ' + this.toCall);
                return;
            }

            this.move(this.betsize);
        },
        call: function(e) {
            this.betsize = this.toCall;
            this.bet(null);
        },
        fold: function(e) {
            this.move(-1);
        },
        addAi: function(e) {
            this.showAiMenu = true;
        },
        leave: function(e) {
            leaveRoom(this.$socket, this.room, this.player.name);
            this.$parent.$emit('leavegame');
        },
        playPause: function(e) {
            this.$emit('playpause', { play: !this.playing });
        },
        move: function(betsize) {
            this.$socket.emit('move', {
                name: this.player.name,
                room: this.room,
                betsize: betsize
            });
        }
    }
}
</script>

<style>

div.top-panel {
    width: 100%;
    position: fixed;
    height: 40px;
    background: #b92323;
    top: 0px;
    left: 0px;
}

div.top-panel > input {
    top: 6px;
    position: relative;
    float: right;
    margin-left: 10px;
    margin-right: 10px;
}

.card-panel {
    display: flex;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
    margin-top: 10px;
    margin-bottom: 10px;
}

.board {
    width: 780px;
}

.hand {
    width: 295px;
}

</style>
