<template>
    <div class="entry" :class="{ visible: visible }" @mouseover="show" @mouseout="lazyHide">
        <template v-if="visible">
            <span class="heading">Hand# {{ handNum }}</span>
            <div class="board">
                <card v-for="(c, i) in board" :key="'boardcard-' + i" :ident="c" :size="30"/>
            </div>
            <p v-for="(w, i) in winners" :key="'content-' + i">
                <span class="content">
                    {{ w.name }} won {{ w.pot }} with <div class="cards"><card :ident="w.hand[0]" :size="15" /><card :ident="w.hand[1]" :size="15" /></div> ({{ w.hand_score }})
                </span>
            </p>
        </template>
    </div>
</template>

<script>
import Card from './Card.vue'

export default {
    name: "SideBarEntry",
    components: {
        Card
    },
    props: {
        handNum: Number,
        winners: Array,
        board: Array,
        minTimeVisible: {
            type: Number,
            default: 750
        }
    },
    data: function() {
        return {
            visible: false,
            timeoutId: null
        }
    },
    methods: {
        show: function() {
            this.clearTimeout();

            this.visible = true;
        },
        lazyHide: function() {
            if (this.timeoutId !== null) {
                return;
            }

            this.timeoutId = setTimeout(this.hide, this.minTimeVisible);
        },
        hide: function() {
            this.clearTimeout();

            this.visible = false;
        },
        clearTimeout: function() {
            if (this.timeoutId !== null) {
                clearTimeout(this.timeoutId);
                this.timeoutId = null;
            }
        }
    }
}
</script>

<style scoped>

.board {
    display: inline-block;
    width: 100%;
    margin-top: 15px;
    margin-bottom: 15px;
}

.cards {
    display: inline
}

.entry {
    background: #b92323;
    display: block;

    right: 0px;
    width: 40px;
    height: 100px;
    border-radius: 21px 0px 0px 21px;

    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: auto;
    margin-right: 0px;

    transition: 0.5s;
}

.visible {
    background: #ffffff;
    width: 700px;
    max-height: 500px;
    overflow: auto;
    height: auto;
    border: 3px;
    border-style: solid;
    border-color: #b92323;
}

.heading {
    font-size: 20px;
    font-weight: 600;
}

</style>
