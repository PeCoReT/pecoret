<script>
import { useAuthStore } from '@/store/auth';

export default {
    name: 'Home',
    created() {
        const authStore = useAuthStore();
        if (authStore.isAuthenticated !== true) {
            this.$router.push({ name: 'Login' });
        } else {
            this.$router.push({ name: 'ProjectList' });
        }
    }
};
</script>
<template></template>
