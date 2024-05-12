<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'LatestTargetCard',
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
                limit: 1,
                ordering: '-date_updated'
            };
            this.service.getTargets(this.$api, this.programId, data).then((response) => {
                if (response.data.results.length > 0) {
                    this.text = response.data.results[0].ip;
                } else {
                    this.text = 'None';
                }
            });
        }
    }
};
</script>

<template>
    <DetailCardWithIcon title="Latest Host" :text="text" icon="fa fa-crosshairs"></DetailCardWithIcon>
</template>
