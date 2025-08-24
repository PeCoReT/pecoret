<script>
export default {
    name: 'LoadingBar',
    props: {
        height: { type: String, default: '2px' },
        bg: { type: String, default: 'bg-muted' },
        color: { type: String, default: 'bg-blue-500' },
        speed: { type: String, default: '1.8s' }
    },
    computed: {
        outerStyle() {
            return { height: this.height };
        },
        innerStyle() {
            return { animationDuration: this.speed };
        }
    }
};
</script>

<template>
    <div class="relative overflow-hidden w-full" :class="bg" :style="outerStyle">
        <div class="absolute top-0 left-0 h-full loading-bar-inner" :class="color" :style="innerStyle"></div>
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

.loading-bar-inner {
    animation-name: loading-bar;
    animation-timing-function: ease;
    animation-iteration-count: infinite;
}
</style>
