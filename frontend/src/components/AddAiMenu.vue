<template>
    <input type="text" v-model="name" :style="styleObj" ref="name" placeholder="Enter name" @keydown.enter="addAi" @blur="$emit('close')">
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
            name: '',
            width: '0px'
        };
    },
    mounted: function() {
        this.width = '300px';
        this.$refs.name.focus();
    },
    computed: {
        styleObj: function() {
            return {
                'width': this.width
            };
        }
    },
    methods: {
        addAi: function(e) {
            joinRoom(this.$socket, this.room, this.name, 'ai').then(
                (resp) => {
                    if (resp.msg) {
                        flash(resp.status, resp.msg);
                    }

                    if (resp.status === 'ok') {
                        this.$emit('close');
                    }
                }
            );
        }
    }
}
</script>

<style scoped>

input {
    position: fixed;
    top: 0;
    padding: 5px;
    font-size: 18px;
    font-weight: bold;
    right: 9px;
    width: 0px;
    transition: 0.25s
}
</style>
