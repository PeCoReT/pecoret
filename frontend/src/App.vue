<script>
export default {
    created() {
        this.$api.get(this.$api.e.authCheck).then((response) => {
            this.$api.updateCSRFToken(response.data);
        });
    }
};
</script>

<template>
    <router-view />
</template>
