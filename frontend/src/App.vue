<script>
import AuthService from '@/service/AuthService';

export default {
    created() {
        const authService = new AuthService();
        authService.checkAuth(this.$api);
    }
};
</script>

<template>
    <router-view />
</template>