<script>
import { defineComponent } from 'vue';
import FindingService from '@/service/FindingService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';

export default defineComponent({
    name: 'DashboardFindingsCount',
    components: { DetailCardWithIcon },
    data() {
        return {
            service: new FindingService(),
            model: {},
            projectId: this.$route.params.projectId,
            loading: false
        };
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            this.loading = true;
            this.service
                .getFindings(this.$api, this.projectId)
                .then((response) => {
                    this.model.count = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
});
</script>

<template>
    <DetailCardWithIcon title="Findings" :text="model.count" icon="fa fa-bugs" styleClass="" :loading="loading"></DetailCardWithIcon>
</template>

<style scoped></style>
