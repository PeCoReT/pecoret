<script>
import AdvisoryService from '@/service/AdvisoryService';
import AdvisoryTabMenu from '@/components/pages/AdvisoryTabMenu.vue';
import AdvisoryTimelineCreateDialog from '@/components/advisories/AdvisoryTimelineCreateDialog.vue';

export default {
    name: 'TimelineList',
    data() {
        return {
            service: new AdvisoryService(),
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Advisory Detail',
                    to: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Timeline',
                    disabled: true
                }
            ],
            advisoryId: this.$route.params.advisoryId,
            items: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.service.getTimeline(this.$api, this.advisoryId).then((response) => {
                this.items = response.data.results;
            });
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this timeline item?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTimeline(this.$api, this.advisoryId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Timeline item was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    components: { AdvisoryTabMenu, AdvisoryTimelineCreateDialog }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <AdvisoryTimelineCreateDialog @object-created="getItems"></AdvisoryTimelineCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card border-noround-top">
                <Timeline :value="items" class="mt-3">
                    <template #opposite="slotProps">
                        <small class="p-text-secondary">{{ slotProps.item.date }}</small>
                    </template>
                    <template #content="slotProps">
                        <a @click="onDeleteConfirmDialog(slotProps.item.pk)">{{ slotProps.item.text }}</a>
                    </template>
                </Timeline>
            </div>
        </div>
    </div>
</template>