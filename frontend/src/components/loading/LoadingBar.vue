<script>
export default {
    name: 'LoadingBar',
    props: {
        // height of the bar
        height: {
            type: String,
            default: '2px'
        },
        // outer background
        bg: {
            type: String,
            default: 'bg-muted'
        },
        // inner (moving) bar color
        color: {
            type: String,
            default: 'bg-muted bg-blue-500'
        },
        speed: {
            type: String,
            default: '1.8s'
        }
    },
    computed: {
        outerStyle() {
            return {
                height: this.height
            };
        },
        innerStyle() {
            return {
                animationDuration: this.speed
            };
        }
    }
};
</script>

<template>
    <div class="relative overflow-hidden w-full" :class="bg" :style="outerStyle">
        <div class="absolute top-0 left-0 h-full" :class="color" :style="innerStyle" />
    </div>
</template>

<style scoped>
@keyframes loading-bar {
    0% {
        left: -30%;
        width: 30%;
    }
    50% {
        left: 35%;
        width: 30%;
    }
    100% {
        left: 100%;
        width: 30%;
    }
}
.loading-bar-enter-active,
.loading-bar-leave-active {
    transition: opacity 0.2s;
}
.loading-bar-enter-from,
.loading-bar-leave-to {
    opacity: 0;
}

/* apply the keyframes to the inner div */
.absolute.top-0.left-0.h-full[style] {
    animation-name: loading-bar;
    animation-timing-function: ease;
    animation-iteration-count: infinite;
}
</style>
