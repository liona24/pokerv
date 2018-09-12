<template>
    <div name="player-hud">
        <div class="top-panel">
            <div class="float-right">
                <input type="button" value="Leave" @click="leave">
                <input type="button" value="Add AI" @click="addAi">
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
            <card v-for="(c, i) in hand" :key="'handcard-' + i" :ident="c"/>
        </div>
        <div class="bet-panel">
            <input type="number" v-model="betsize" name="betsize">
            <input type="button" value="Bet" @click="bet">
            <input type="button" value="Call" @click="call">
            <input type="button" value="Fold" @click="fold">
        </div>
    </div>
</template>

<script>
import Card from './Card.vue'

export default {
    name: 'PlayerHud',
    components: {
        Card
    },
    props: {
        board: Array,
        hand: Array,
        playing: Boolean
    },
    data: function() {
        return {
            betsize: 0
        };
    },
    methods: {
        bet: function(e) {

        },
        call: function(e) {

        },
        fold: function(e) {

        },
        addAi: function(e) {

        },
        leave: function(e) {

        },
        playPause: function(e) {
            this.$emit('playpause', { play: !this.playing });
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
