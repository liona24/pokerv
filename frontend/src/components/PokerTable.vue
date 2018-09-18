<template>
    <div>
        <canvas ref="canvas" :width="width" :height="height"></canvas>
    </div>
</template>

<script>

export default {
    name: 'PokerTable',
    props: {
        players: Array,
        front: Number,
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
                let n = this.players.length;

                let ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                let delta = Math.PI * 2 / n;

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

                if (n < 2) {
                    ctx.fillText('It seems like you do not have any friends :(', rx, ry);
                    return;
                }

                for (let i = 1; i <= n; i++) {
                    let x = sx * Math.sin(delta * i);
                    let y = sy * Math.cos(delta * i);

                    let j = (i + this.front) % n;
                    let player = this.players[j];

                    if (player.bet) {
                        if (player.is_allin) {
                            ctx.fillStyle = "#b92323";
                        }
                        ctx.fillText(player.bet, rx + sbet * x, ry + sbet * y);
                        if (player.is_allin) {
                            ctx.fillStyle = '#002323';
                        }
                    }
                    if (!player.has_folded) {
                        ctx.fillText(`${player.name} (${player.stack})`, rx + sname * x, ry + sname * y);

                        if (player.action_required) {
                            turnx = rx + sname * x;
                            turny = ry + sname * y;
                            ctx.beginPath();
                            ctx.lineWidth = 5;
                            ctx.strokeStyle = '#b92323';
                            ctx.ellipse(turnx, turny, sturn * sx, sturn * sy, 0, 0, Math.PI * 2);
                            ctx.stroke();
                        }
                    } else {
                        ctx.fillText('Fold', rx + sname * x, ry + sname * y);
                    }
                }

                if (n === 2) {
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

            }
        }
    }
}
</script>

<style>

</style>
