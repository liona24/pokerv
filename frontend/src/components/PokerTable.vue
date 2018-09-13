<template>
    <div>
        <canvas ref="canvas" :width="width" :height="height"></canvas>
    </div>
</template>

<script>

/*
playerInfoLayout = {
    name: String,
    stack: Number,
    bet: Number,
    folded: Boolean
}
*/

export default {
    name: 'PokerTable',
    props: {
        players: Array,
        front: Number,
        active: Number,
        pot: Number,
        width: {
            type: Number,
            default: 800
        },
        height: {
            type: Number,
            default: 600
        },
    },
    data: function() {
        return {};
    },
    mounted: function() {
        this.updateTable();
    },
    watch: {
        players: function() {
            this.updateTable();
        }
    },
    methods: {
        updateTable: function() {
            let canvas = this.$refs.canvas;

            if (canvas && canvas.getContext) {
                let ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                let delta = Math.PI * 2 / this.players.length;

                let sx = 0.7 * canvas.width / 2;
                let sy = 0.7 * canvas.height / 2;

                let rx = canvas.width / 2;
                let ry = canvas.height / 2;

                let sbet = 0.6;
                let sname = 1.2;
                let sturn = 0.3;

                let turnx = null;
                let turny = null;

                ctx.textAlign = 'center';
                ctx.font = "bold 15px 'Avenir', Helvetica, Arial, sans-serif";

                if (this.players.length < 2) {

                    ctx.fillText('It seems like you do not have any friends :(', rx, ry);
                    return;
                }

                ctx.fillText(this.pot, rx, ry);

                for (let i = 1; i <= this.players.length; i++) {
                    let x = sx * Math.sin(delta * i);
                    let y = sy * Math.cos(delta * i);

                    let j = (i + this.front) % this.players.length;
                    let player = this.players[j];

                    ctx.fillText(`${player.name} (${player.stack})`, rx + sname * x, ry + sname * y);
                    if (player.bet) {
                        ctx.fillText(player.bet, rx + sbet * x, ry + sbet * y);
                    }

                    if (i === this.active) {
                        turnx = rx + sname * x;
                        turny = ry + sname * y;
                    }
                }

                let n = this.players.length;
                if (this.players.length === 2) {
                    n = 4;
                    delta /= 2;
                }
                ctx.moveTo(rx, ry);
                ctx.beginPath();
                ctx.strokeStyle = '#002323';
                ctx.lineWidth = 1;

                for (let i = 1; i <= n; i++) {
                    ctx.lineTo(rx + sx * Math.sin(delta * i), ry + sy * Math.cos(delta * i));
                }
                ctx.closePath();
                ctx.stroke();

                ctx.beginPath();
                ctx.lineWidth = 5;
                ctx.strokeStyle = '#b92323';
                if (turnx && turny) {
                    ctx.ellipse(turnx, turny, sturn * sx, sturn * sy, 0, 0, Math.PI * 2);
                }
                ctx.stroke();
            }
        }
    }
}
</script>

<style>

</style>
