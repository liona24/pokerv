<template>
    <div class="entry" :class="{ visible: visible }" @mouseover="show" @mouseout="lazyHide">
        <template v-if="visible">
            <span class="heading">{{ heading }}</span>
            <p v-for="(p, i) in content" :key="'content-' + i">
                <span class="content">
                    {{ p }}
                </span>
            </p>
            <a href="javascript:void(0)" @click="hide">&times;</a>
        </template>
    </div>
</template>

<script>
export default {
    name: "SideBarEntry",
    props: {
        heading: String,
        content: Array,
        minTimeVisible: {
            type: Number,
            default: 1000
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
