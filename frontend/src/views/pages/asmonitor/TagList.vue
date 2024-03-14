<script>
import ASMonitorService from '@/service/ASMonitorService';
import BlankSlate from '@/components/BlankSlate.vue';
import TagCreateDialog from '@/components/asmonitor/TagCreateDialog.vue';
import AdvisoryLabelBadge from '@/components/AdvisoryLabelBadge.vue';
import TagUpdateDialog from '@/components/asmonitor/TagUpdateDialog.vue';

export default {
    name: 'TagList',
    components: { TagUpdateDialog, TagCreateDialog, BlankSlate, AdvisoryLabelBadge },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Tags',
                    disabled: true
                }
            ],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            service: new ASMonitorService(),
            items: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getTags(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getTags(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this tag?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTag(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Tag was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <TagCreateDialog @object-created="this.getItems"></TagCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable :striped-rows="true" :paginator="true" dataKey="pk" :rowHover="items.length > 0" :rows="pagination.limit" :value="items" filterDisplay="menu" :lazy="true" :loading="loading" @page="onPage" :totalRecords="totalRecords">
                    <template #empty>
                        <BlankSlate icon="fa fa-tags" title="No Tags!" text="No Tags found!"></BlankSlate>
                    </template>
                    <template #header>
                        <div class="grid">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <Column field="name" header="Name"></Column>
                    <Column field="description" header="Description"></Column>
                    <Column header="Preview">
                        <template #body="slotProps">
                            <AdvisoryLabelBadge :label="slotProps.data"></AdvisoryLabelBadge>
                        </template>
                    </Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <TagUpdateDialog :tag="slotProps.data" @object-updated="getItems"></TagUpdateDialog>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
