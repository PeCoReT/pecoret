<script>
import { defineComponent } from 'vue';
import LabelCreateDialog from '@/components/dialogs/advisories/LabelCreateDialog.vue';
import AdvisoryLabelBadge from '@/components/badges/AdvisoryLabelBadge.vue';
import LabelUpdateDialog from '@/components/dialogs/advisories/LabelUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import BlankSlate from "@/components/BlankSlate.vue";

export default defineComponent({
    name: 'LabelList',
    components: {
        BlankSlate,
        GenericDataTable,
        BaseListLayout,
        LabelUpdateDialog,
        LabelCreateDialog,
        AdvisoryLabelBadge
    },
    data() {
        return {
            loading: false,
            breadcrumbs: [
                {
                    label: 'Labels',
                    disabled: true
                }
            ],
            searchInput: null,
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
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(query) {
            let params = {
                search: query
            };
            this.$api.get(this.$api.e.aLabelList, null, params).then((response) => {
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
                    this.$api.delete(this.$api.e.aLabelDetail, { pk: id }).then(() => {
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
            this.$api
                .get(this.$api.e.aLabelList, null, params)
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
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <LabelCreateDialog @object-created="getItems"></LabelCreateDialog>
        </template>
        <template #table>
            <div class="sm:w-full md:w-1/3 mb-3">
                <InputGroup>
                    <InputText v-model="searchInput" placeholder="Keyword Search" style="width: 100%" v-on:keyup.enter="onSearch(searchInput)" />
                    <Button icon="fa fa-search" severity="secondary" outlined @click="onSearch(searchInput)"></Button>
                </InputGroup>
            </div>

            <DataView :value="items" v-if="items.length > 0">
                <template #list="slotProps">
                    <div class="col-span-12 rounded border border-surface-700 p-1 hover:bg-surface-950 card m-0" v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex p-4 gap-4">
                            <div class="flex items-center w-1/3">
                                <AdvisoryLabelBadge :label="item"></AdvisoryLabelBadge>
                            </div>
                            <div class="flex items-center w-2/3">
                                {{ item.description }}
                            </div>

                            <div class="flex items-center justify-between"></div>
                            <div class="flex items-center justify-end">
                                <LabelUpdateDialog :label="item" @object-updated="getItems"></LabelUpdateDialog>
                                <Button size="small" outlined label="Delete" severity="danger" @click="confirmDialogDelete(item.pk)" class="p-0 m-0"></Button>
                            </div>
                        </div>
                    </div>
                </template>
                <template #footer>
                    <Paginator :rows="pagination.limit" :totalRecords="totalRecords" @page="onPage"></Paginator>
                </template>
            </DataView>
            <BlankSlate title="No Labels!" text="No labels found!" icon="fa fa-tag" v-else></BlankSlate>
        </template>
    </BaseListLayout>
</template>
