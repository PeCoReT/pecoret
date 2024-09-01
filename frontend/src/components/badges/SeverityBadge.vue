<script>
export default {
    name: 'SeverityBadge',
    props: ['severity'],
    computed: {
        getClasses() {
            return 'severity-badge severity-' + this.severity.toLowerCase();
        }
    }
};
</script>
<template>
    <span :class="getClasses">{{ this.severity }}</span>
</template>
