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
      state: "GAME",
      room: "Lion's Room",
      user: "Lion"
    }
  },
  socket: {
    messageChannel: function(msg) {
      flash('ok', msg);
    }
  },
  methods: {
    joinGame: function(e) {
      this.state = 'GAME';
      this.user = e.user;
      this.room = e.room;
    },
    leaveGame: function(e) {
      this.state = 'HOME';
      this.room = '';
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
</style>
