<script>
export default {
    name: 'CountryFlag',
    props: {
        countryCode: {
            required: true
        }
    }
};
</script>

<template>
    <span :class="'mr-2 text-xl fi fi-' + countryCode.toLocaleLowerCase()"></span>
</template>

<style scoped>
@import '@/../node_modules/flag-icons/css/flag-icons.css';
</style>
