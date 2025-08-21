<script>
import { Navbar } from '@/components/navbar';

export default {
    name: 'AdvisorySubMenu',
    components: { Navbar },
    data() {
        return {
            items: [
                {
                    label: 'Dashboard',
                    icon: 'fa fa-dashboard',
                    route: this.$router.resolve({
                        name: 'AdvisoryDashboard'
                    })
                },
                {
                    label: 'Advisory List',
                    icon: 'fa fa-bugs',
                    route: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Labels',
                    icon: 'fa fa-tags',
                    route: this.$router.resolve({ name: 'AdvisoryLabelList' })
                }
            ]
        };
    }
};
</script>

<template>
    <Navbar :items="items"></Navbar>
</template>
