<script>
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'LatestFindings',
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
                ordering: '-date_created'
            };
            this.service.getFindings(this.$api, this.programId, data).then((response) => {
                this.items = response.data.results;
            });
        },
        onItemClick(id) {
            this.$router.push({
                name: 'ASMonitorFindingDetail',
                params: {
                    programId: this.programId,
                    findingId: id
                }
            });
        }
    }
};
</script>

<template>
    <Card class="card p-1">
        <template #title>Latest Findings</template>
        <template #content>
            <DataView :value="items">
                <template #list="slotProps">
                    <div class="col-12 border-round border-1 p-0 hover:surface-hover card m-0" @click="onItemClick(item.pk)" v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex p-4 gap-4">
                            <div class="flex justify-content-start w-full">
                                {{ item.name }}
                            </div>

                            <div class="flex align-items-center justify-content-end">
                                <span class="severity-badge" :class="'severity-' + item.severity.toLowerCase()">{{ item.severity }}</span>
                            </div>
                        </div>
                    </div>
                </template>
            </DataView>
        </template>
    </Card>
</template>
