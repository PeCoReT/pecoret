<script>
export default {
    name: 'SettingsTabMenu',
    data() {
        return {
            items: [
                {
                    label: 'General & Notifications',
                    route: this.$router.resolve({
                        name: 'UserSettingsDetail'
                    })
                },
                {
                    label: 'Profile',
                    route: this.$router.resolve({
                        name: 'UserProfileSettings'
                    })
                },
            ]
        };
    }
};
</script>

<template>
    <pTabMenu v-model="items"></pTabMenu>
</template>