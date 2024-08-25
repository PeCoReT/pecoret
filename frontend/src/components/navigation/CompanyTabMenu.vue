<script>
export default {
    name: 'CompanyTabMenu',
    data() {
        return {
            items: [
                {
                    label: 'Details',
                    route: this.$router.resolve({
                        name: 'CompanyDetail',
                        params: {
                            companyId: this.$route.params.companyId
                        }
                    })
                },
                {
                    label: 'Contacts',
                    route: this.$router.resolve({
                        name: 'CompanyContactList',
                        params: {
                            companyId: this.$route.params.companyId
                        }
                    })
                }
            ]
        };
    }
};
</script>

<template>
    <pTabMenu v-model="items"></pTabMenu>
</template>