<script>
export default {
    name: 'ScanStatusBadge',
    props: {
        status: {
            required: true
        }
    },
    computed: {
        cssClasses() {
            if (this.status === 'Running') {
                return 'bg-yellow-500 text-gray-900';
            } else if (this.status === 'Completed') {
                return 'bg-green-500 text-gray-900';
            } else if (this.status === 'Failed') {
                return 'bg-red-500 text-gray-900';
            }
            return 'bg-cyan-500 text-gray-900';
        }
    }
};
</script>

<template>
    <span :className="'inline-block text-sm px-3 py-1 rounded-full ' + this.cssClasses">{{ status }}</span>
</template>
