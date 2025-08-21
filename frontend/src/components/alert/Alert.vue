<script>
export default {
    name: 'AlertPanel',
    data() {
        return {
            isVisible: true
        };
    },
    props: {
        message: {
            type: String,
            required: true
        },
        type: {
            type: String,
            default: 'info' // Can be 'info', 'success', 'error', 'warning'
        }
    },
    computed: {
        alertClasses() {
            switch (this.type) {
                case 'success':
                    return 'bg-green-100 text-green-800 border border-green-400';
                case 'error':
                    return 'bg-red-100 text-red-800 border border-red-400';
                case 'warning':
                    return 'bg-yellow-100 text-yellow-800 border border-yellow-400';
                default:
                    return 'bg-blue-100 text-blue-800 border border-blue-400';
            }
        }
    },
    methods: {
        closeAlert() {
            this.isVisible = false;
        }
    }
};
</script>
<template>
    <div v-if="isVisible" :class="['alert', alertClasses]" class="flex items-center justify-between p-4 mb-4 text-sm rounded-lg" role="alert">
        <slot>
            <span>{{ message }}</span>
        </slot>
        <button class="text-xl font-bold leading-none focus:outline-none" @click="closeAlert">&times;</button>
    </div>
</template>

<style scoped>
button {
    background: transparent;
    border: none;
    cursor: pointer;
}
</style>
