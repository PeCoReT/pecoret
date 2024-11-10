<script>
import AdvisoryTabMenu from '@/components/navigation/AdvisoryTabMenu.vue';
import AdvisoryTimelineCreateDialog from '@/components/dialogs/advisories/AdvisoryTimelineCreateDialog.vue';

export default {
    name: 'TimelineList',
    data() {
        return {
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
            this.$api.get(this.$api.e.aTimelineList, { aPk: this.advisoryId }).then((response) => {
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
                    this.$api.delete(this.$api.e.aTimelineDetail, { aPk: this.advisoryId, pk: id }).then(() => {
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
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-6">
            <div class="flex justify-start"></div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <AdvisoryTimelineCreateDialog @object-created="getItems"></AdvisoryTimelineCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <AdvisoryTabMenu></AdvisoryTabMenu>
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
