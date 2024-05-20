<script>
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'LatestTargets',
    props: {
        programId: {
            required: true
        }
    },
    data() {
        return {
            loading: false,
            service: new ASMonitorService(),
            loaded: false,
            items: []
        };
    },
    watch: {
        programId: {
            handler(value) {
                if (value && this.loaded === false) {
                    this.loaded = true;
                    this.getItems();
                }
            }
        }
    },
    methods: {
        getItems() {
            let data = {
                limit: 5,
                ordering: '-date_updated'
            };
            this.service.getTargets(this.$api, this.programId, data).then((response) => {
                this.items = response.data.results;
            });
        },
    }
};
</script>

<template>
    <Card class="card p-1">
        <template #title>Latest Hosts</template>
        <template #content>
            <DataView :value="items">
                <template #list="slotProps">
                    <div class="col-12 border-round border-1 p-0 card m-0" v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex p-4 gap-4">
                            <div class="flex justify-content-start w-full">
                                {{ item.name }} ({{ item.ip }})
                            </div>
                        </div>
                    </div>
                </template>
            </DataView>
        </template>
    </Card>
</template>
