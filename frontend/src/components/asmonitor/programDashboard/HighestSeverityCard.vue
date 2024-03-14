<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'HighestSeverityCard',
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
            let data = {
                ordering: '-severity',
                limit: 1
            };
            this.service.getFindings(this.$api, this.programId, data).then((response) => {
                if (response.data.results.length > 0) {
                    this.text = response.data.results[0].severity;
                } else {
                    this.text = 'None';
                }
            });
        }
    }
};
</script>

<template>
    <DetailCardWithIcon title="Highest Severity" :text="text" icon="fa fa-bolt"></DetailCardWithIcon>
</template>
