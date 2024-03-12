<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'FindingCount',
    components: { DetailCardWithIcon },
    props: {
        programId: {
            required: true
        }
    },
    data() {
        return {
            text: '-',
            service: new ASMonitorService(),
            loaded: false
        };
    },
    watch: {
        programId: {
            handler(value) {
                if (value && this.loaded === false) {
                    this.loaded = true;
                    this.getFindingsCount();
                }
            }
        }
    },
    methods: {
        getFindingsCount() {
            this.service.getFindings(this.$api, this.programId, { limit: 1 }).then((response) => {
                this.text = response.data.count;
            });
        }
    }
};
</script>

<template>
    <DetailCardWithIcon title="Findings" :text="text" icon="fa fa-bug"></DetailCardWithIcon>
</template>
