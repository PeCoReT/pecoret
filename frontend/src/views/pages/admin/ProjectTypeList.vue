<script>
import ProjectTypeUpdateDialog from '@/components/dialogs/ProjectTypeUpdateDialog.vue';
import ProjectTypeCreateDialog from '@/components/dialogs/ProjectTypeCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'ProjectTypeList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Project Types',
                    disabled: true
                }
            ],
            loading: false,
            pagination: { page: 1, limit: 20 },
            totalRecords: 0,
            items: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems() {
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.$api
                .get(this.$api.e.pentestTypeList, null, params)
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
                message: 'Do you want to delete this project type?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.pentestTypeDetail, { pk: id }).then(() => {
                        this.$toast.add({
                            severity: 'success',
                            summary: 'Deleted',
                            detail: 'Project type was deleted successfully!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    components: { ProjectTypeUpdateDialog, ProjectTypeCreateDialog, BlankSlate }
};
</script>

<template>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-6">
            <div class="justify-start flex"></div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <ProjectTypeCreateDialog @object-created="getItems"></ProjectTypeCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <Card>
                <template #content>
                    <DataTable paginator :rowHover="items.length > 0" :rows="pagination.limit" :value="items" lazy dataKey="pk" filterDisplay="menu" :totalRecords="totalRecords" :loading="loading" @page="onPage" responsiveLayout="scroll">
                        <Column field="name" header="Name"></Column>
                        <Column header="Actions">
                            <template #body="slotProps">
                                <ProjectTypeUpdateDialog :pentest-type="slotProps.data"></ProjectTypeUpdateDialog>
                                <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                            </template>
                        </Column>
                        <template #empty>
                            <BlankSlate icon="fa fa-icons" title="No Project Types!" text="No project types found!"></BlankSlate>
                        </template>
                    </DataTable>
                </template>
            </Card>
        </div>
    </div>
</template>
