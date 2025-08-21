<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/select';
import { Paginator } from '@/components/paginator';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'ScopeList',
    mixins: [listViewMixin],
    mounted() {
        this.getItems();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            showCreateForm: false,
            newScope: {
                details: null,
                permission: null
            },
            scopePermissions: [
                {
                    label: 'Allowed',
                    value: 'Allowed'
                },
                {
                    label: 'Denied',
                    value: 'Denied'
                }
            ]
        };
    },
    methods: {
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to delete this scope?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteScope(id);
                }
            });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pScopeList, { projectPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        deleteScope(id) {
            this.$api.delete(this.$api.e.pScopeDetail, { projectPk: this.projectId, pk: id }).then(() => {
                this.$toaster({
                    title: 'Deleted',
                    description: 'Scope was deleted!',
                    duration: 3000
                });
                this.getItems();
            });
        },
        create() {
            this.$api.post(this.$api.e.pScopeList, { projectPk: this.projectId }, this.newScope).then(() => {
                this.$toaster({
                    title: 'Scope created!',
                    duration: 3000,
                    description: 'Scope created successfully'
                });
                this.newLabel = { details: null, permission: null };
                this.showCreateForm = false;
                this.getItems();
            });
        }
    },
    components: {
        DataViewHeader,
        Paginator,
        Label,
        Input,
        Button,
        DataViewContent,
        DataViewListLayout,
        Select
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #create-button>
            <Button
                @click="
                    () => {
                        this.showCreateForm = true;
                    }
                "
                ><i class="fa fa-plus"></i> Scope
            </Button>
        </template>
        <div v-if="showCreateForm === true" class="mt-3">
            <div class="flex flex-wrap md:flex-nowrap items-stretch gap-4 mt-3">
                <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                    <Label class="text-sm font-medium" for="name">Details</Label>
                    <Input id="name" v-model="newScope.details"></Input>
                </div>

                <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                    <Label class="text-sm font-medium" for="description">Permissions</Label>
                    <Select v-model="newScope.permission" :options="scopePermissions"></Select>
                </div>

                <!-- Save and Cancel Buttons (Right Aligned) -->
                <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
                    <Button
                        variant="outline"
                        @click="
                            () => {
                                this.showCreateForm = false;
                            }
                        "
                        >Cancel
                    </Button>
                    <Button variant="default" @click="create">Save</Button>
                </div>
            </div>
        </div>
        <DataViewHeader :total-records="totalRecords"></DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-star" blank-slate-text="No scopes found!" blank-slate-title="No Scopes!">
            <template #item="{ item }">
                <span v-if="item.permission === 'Allowed'">
                    <i class="h-4 w-4 text-success fa fa-check" />
                </span>
                <span v-else> <i class="h-4 w-4 text-destructive fa fa-cancel" /></span>
                <div class="flex-1">
                    {{ item.details }}
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
