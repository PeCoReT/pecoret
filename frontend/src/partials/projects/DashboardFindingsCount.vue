<script>
import { defineComponent } from 'vue';
import { DetailCardWithIcon } from '@/components/card';

export default defineComponent({
    name: 'DashboardFindingsCount',
    components: { DetailCardWithIcon },
    data() {
        return {
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
            this.$api
                .get(this.$api.e.pFindingList, { pPk: this.projectId })
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
    <DetailCardWithIcon :loading="loading" :text="model.count" icon="fa fa-bugs" styleClass="" title="Findings"></DetailCardWithIcon>
</template>
