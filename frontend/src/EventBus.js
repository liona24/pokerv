import Vue from 'vue'

export const EventBus = new Vue();

export function flash(status, msg) {
    console.log(`flash ( ${status}, ${msg} )`);
    EventBus.$emit('flash', { status: status, msg: msg });
}
