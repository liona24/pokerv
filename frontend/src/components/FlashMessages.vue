<template>
    <div id="flash-messages">
        <span v-for="(item, index) in messages" class="message" :class="item.status" :key="'flash-' + index">{{ item.msg }}</span>
    </div>
</template>

<script>

import { EventBus } from "../EventBus.js";

export default {
    name: 'FlashMessages',
    data: function() {
        return {
            messages: []
        }
    },
    created: function() {
        EventBus.$on('flash', this.addFlashMessage);
    },
    methods: {
        addFlashMessage: function(msg) {
            this.messages.push(msg);
            setTimeout(() => {
                this.messages.splice(this.messages.indexOf(msg), 1);;
            }, 2000);
        }
    }
}
</script>

<style scoped>

div#flash-messages {
    position: fixed;
    left: 0;
    top: 69px;
    width: 100%;
    z-index: 99999;
}

.message {
    text-align: center;
    margin-bottom: 7px;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 20px;
    font-weight: bold;
    font-size: 14px;
    display: block;
}
.ok {
    background: rgba(76, 175, 79, 0.651);
}
.err {
    background: rgba(230, 0, 0, 0.651);
}
</style>
