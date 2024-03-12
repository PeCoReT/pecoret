<script>
import { defineComponent } from 'vue';
import AdvisoryService from '@/service/AdvisoryService';
import BlankSlate from '@/components/BlankSlate.vue';
import AdvisoryManagementLabelCreateDialog from '@/components/dialogs/AdvisoryManagementLabelCreateDialog.vue';
import AdvisoryLabelBadge from '@/components/AdvisoryLabelBadge.vue';
import AdvisoryManagementLabelUpdateDialog from '@/components/dialogs/advisory-management/AdvisoryManagementLabelUpdateDialog.vue';

export default defineComponent({
    name: 'LabelList',
    components: {
        AdvisoryManagementLabelUpdateDialog,
        AdvisoryManagementLabelCreateDialog,
        BlankSlate,
        AdvisoryLabelBadge
    },
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            breadcrumbs: [
                {
                    label: 'Labels',
                    disabled: true
                }
            ],
            items: [],
            totalRecords: 0,
            pagination: { page: 1, limit: 25 },
            filters: {}
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onSort(event) {},
        onFilter(event) {},
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.service.getLabels(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this label?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteLabel(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Label was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getLabels(this.$api, params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
});
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
                <AdvisoryManagementLabelCreateDialog @object-created="getItems"></AdvisoryManagementLabelCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    paginator
                    lazy
                    dataKey="pk"
                    :value="items"
                    :rows="pagination.limit"
                    :row-hover="items.length > 0"
                    :totalRecords="totalRecords"
                    filterDisplay="menu"
                    :loading="loading"
                    @sort="onSort"
                    @page="onPage"
                    @filter="onFilter"
                    v-model:filters="filters"
                >
                    <template #header>
                        <div class="grid">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <template #empty>
                        <BlankSlate icon="fa fa-tags" text="No labels found!" title="No labels!"></BlankSlate>
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
                            <AdvisoryManagementLabelUpdateDialog :label="slotProps.data" @object-updated="getItems"></AdvisoryManagementLabelUpdateDialog>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
