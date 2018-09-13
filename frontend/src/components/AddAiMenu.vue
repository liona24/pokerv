<template>
    <div>
        <input type="text" v-model="name" ref="name" placeholder="Enter name" @keydown.enter="addAi">
    </div>
</template>

<script>
import { joinRoom } from '../communication.js'
import { flash } from '../EventBus.js'

export default {
    name: "AddAiMenu",
    props: {
        room: String
    },
    data: function() {
        return {
            name: ''
        };
    },
    mounted: function() {
        this.$refs.name.focus();
    },
    methods: {
        addAi: function(e) {
            joinRoom(this.$socket, this.room, this.name, 'ai').then(
                (status, code, msg) => {
                    if (msg) {
                        flash(status, msg);
                    }

                    if (status === 'ok') {
                        this.$emit('close');
                    }
                }
            );
        }
    }
}
</script>

<style>

</style>
