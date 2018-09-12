<template>
    <div :class="{ 'red-border': suit == 'h' || suit == 'd' }">
        <img v-if="suit == 'h'" src="../assets/h.png">
        <img v-else-if="suit == 'd'" src="../assets/d.png">
        <img v-else-if="suit == 'c'" src="../assets/c.png">
        <img v-else-if="suit == 's'" src="../assets/s.png">
        <span :class="{ red: suit == 'h' || suit == 'd' }">{{ rank }}</span>
    </div>
</template>

<script>
export default {
    name: "Card",
    props: {
        ident: String
    },
    computed: {
        suit: function() {
            return this.ident[0];
        },
        rank: function() {
            return this.ident[1];
        }
    }

}
</script>

<style scoped>
div {
    display: flex;
    align-items: center;
    float: left;
    border-style: solid;
    padding-right: 10px;
    margin-left: 3px;
    margin-right: 3px;
    border-color: #002323
}

img {
    width: 70px;
    height: 70px
}

span {
    font-size: 70px;
    font-weight: bold;
    padding-left: 13px;
    color: #002323
}

.red-border {
    border-color: #b92323
}

.red {
    color: #b92323
}

</style>
