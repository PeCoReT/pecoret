<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'TargetCountCard',
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
                    this.getItemsCount();
                }
            }
        }
    },
    methods: {
        getItemsCount() {
            let data = {
                limit: 1
            };
            this.loaded = true;
            this.service.getTargets(this.$api, this.programId, data).then((response) => {
                this.text = response.data.count;
            });
        }
    }
};
</script>

<template>
    <DetailCardWithIcon title="Targets" :text="text" icon="fa fa-crosshairs"></DetailCardWithIcon>
</template>
