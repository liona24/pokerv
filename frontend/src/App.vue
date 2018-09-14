<template>
  <div id="app">
    <flash-messages />
    <home v-if="state == 'HOME'" @joingame="joinGame" :user="user" :room="room"/>
    <game v-else-if="state == 'GAME'" @leavegame="leaveGame" :user="user" :room="room"/>
  </div>
</template>

<script>
import Home from './components/Home.vue'
import Game from './components/Game.vue'
import FlashMessages from './components/FlashMessages.vue'

import { flash } from "./EventBus.js";

export default {
  name: 'app',
  components: {
    Home,
    Game,
    FlashMessages
  },
  data: function() {
    return {
      state: "HOME",
      room: "Lion's Room",
      user: "Lion"
    }
  },
  created: function() {
    this.$socket.on('message', this.onMessage);
  },
  beforeDestroy: function() {
    this.$socket.off('message', this.onMessage);
  },
  methods: {
    joinGame: function(e) {
      this.state = 'GAME';
      this.user = e.user;
      this.room = e.room;
    },
    leaveGame: function(e) {
      this.state = 'HOME';
    },
    onMessage: function(msg) {
      flash('ok', msg);
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #002323;
  margin-top: 60px;
}

.float-left {
    float: left
}

.float-right {
    float: right
}
</style>
