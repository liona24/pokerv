<template>
    <div class="status-side-bar">
        <side-bar-entry v-for="(e, i) in entries"
            :key="'side-bar-entry-' + i"
            :content="e.content"
            :heading="e.heading"
            :min-time-visible="entryMinTimeVisible"
            />
    </div>
</template>

<script>
import SideBarEntry from './SideBarEntry.vue'

import { EventBus } from "../EventBus.js";

export default {
    name: "StatusSideBar",
    components: {
        SideBarEntry
    },
    props: {
        maxNumberEntries: {
            default: 5,
            type: Number
        },
        entryMinTimeVisible: {
            type: Number,
            default: 1000
        }
    },
    data: function() {
        return {
            entries: []
        }
    },
    created: function() {
        EventBus.$on('status', this.addEntry);
    },
    methods: {
        addEntry: function(entry) {
            this.entries.push(entry);
            if (this.entries.length > this.maxNumberEntries) {
                this.entries.splice(0, 1);
            }
        }
    }
}
</script>

<style soped>

.status-side-bar {
    position: fixed;
    right: 0px;
    height: 100%;
    top: 69px;
    z-index: 99999;
}

</style>
