<template>
    <div>
    <h1>Welcome!</h1>

    <p>Choose to either <span class="text-heading">create</span> a new room or <span class="text-heading">join</span> an existing one!</p>

    <label>
        <span>Username:</span>
        <input type="text" v-model="user" name="username">
    </label>
    <br>
    <label>
        <span>Room:</span>
        <input type="text" v-model="room" name="roomname">
    </label>
    <br>
    <br>
    <label>
        <span>Stack Size:</span>
        <input type="number" v-model="stacksize" name="stacksize">
    </label>
    <br>
    <label>
        <span>Big Blind:</span>
        <input type="number" v-model="bblind" name="bblind">
    </label>
    <br>
    <label>
        <span>Small Blind:</span>
        <input type="number" v-model="sblind" name="sblind">
    </label>
    <br>
    <br>
    <input type="button" value="Create" @click="create">
    <input type="button" value="Join" @click="join">
    </div>
</template>

<script>

import { createRoom } from '../communication.js'
import { flash } from '../EventBus.js'

export default {
    name: "Home",
    props: {
        room: String,
        user: String
    },
    data: function() {
        return {
            stacksize: 100,
            bblind: 2,
            sblind: 1,
            socket: null,
        }
    },
    methods: {
        create: function(e) {
            if (!this.isInputValid()) {
                return;
            }

            createRoom(this.$socket, this.room, 6, this.stacksize,
                       this.bblind, this.sblind).then(
                (resp) => {
                    if (resp.msg) {
                        flash(resp.status, resp.msg);
                    }

                    if (resp.status === 'ok') {
                        this.join();
                    }
                }
            );
        },
        join: function(e) {
            if (!this.isInputValid()) {
                return;
            }

            this.$emit('joingame', {
                user: this.user,
                room: this.room
            });
        },
        isInputValid: function() {
            return this.room.length > 0 &&
                   this.user.length > 0;
        }
    }
}
</script>

<style>
</style>
