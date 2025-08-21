<script>
import { findingComponentStatus } from '@/utils/constants';
import { Button } from '@/components/ui/button';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import { Select } from '@/components/select';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'AffectedComponentFindingCard',
    mixins: [listViewMixin],
    components: {
        Label,
        Input,
        ModelCombobox,
        DataViewHeader,
        DataViewContent,
        SearchField,
        Button,
        Select
    },
    data() {
        return {
            findingId: this.$route.params.findingId,
            items: [],
            loading: false,
            newComponent: {
                finding: this.$route.params.findingId,
                data: null
            },
            filters: {
                search: { value: null }
            },
            showCreateForm: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 50 },
            selectedItems: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        findingComponentStatus() {
            return findingComponentStatus;
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(query) {
            this.getItems({ search: query });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            data['finding'] = this.findingId;
            this.$api
                .get(this.$api.e.asFindingComponentList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        patchComponent(data) {
            this.$api.patch(this.$api.e.asFindingComponentDetail, { pk: data.pk }, { status: data.status }).then(() => {
                this.$toaster({
                    duration: 3000,
                    title: 'Component updated!',
                    description: 'Component updated successfully!'
                });
            });
        },
        async bulkDelete() {
            this.$confirm.require({
                accept: async () => {
                    let itemsDeleted = 0;
                    let totalLength = Object.entries(this.selectedItems).length;
                    for (const [key, value] of Object.entries(this.selectedItems)) {
                        itemsDeleted++;
                        if (value === true) {
                            await this.$api
                                .delete(this.$api.e.asFindingComponentDetail, {
                                    pk: key
                                })
                                .then(() => {
                                    if (itemsDeleted === totalLength) {
                                        this.selectedItems = {};
                                        this.getItems();
                                    }
                                });
                        }
                    }
                }
            });
        },
        create() {
            this.$api.post(this.$api.e.asFindingComponentList, null, this.newComponent).then(() => {
                this.$toaster({
                    title: 'Component created!',
                    duration: 3000,
                    description: 'Component created successfully!'
                });
                this.$emit('object-created');
                this.showCreateForm = false;
                this.getItems();
            });
        }
    }
};
</script>

<template>
    <h2 class="text-xl font-semibold mb-3 mt-10">Affected Components</h2>

    <div class="col-span-12">
        <div class="flex justify-between items-center w-full gap-2">
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
            <Button
                @click="
                    () => {
                        this.showCreateForm = true;
                    }
                "
            >
                <i class="fa fa-plus" /> Component
            </Button>
        </div>
    </div>

    <Card v-if="showCreateForm === true" class="col-span-12">
        <div>
            <div class="flex flex-wrap items-stretch">
                <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                    <Label class="text-sm font-medium" for="name">Component</Label>
                    <Input v-model="newComponent.data"></Input>
                </div>

                <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
                    <Button variant="outline" @click="this.showCreateForm = false">Cancel</Button>
                    <Button variant="default" @click="create">Save</Button>
                </div>
            </div>
        </div>
    </Card>
    <DataViewHeader :total-records="totalRecords" :show-bulk-select="true" v-model:items="items" v-model:selection="selectedItems">
        <template #bulk>
            <Button @click="bulkDelete" variant="destructive">Delete</Button>
        </template>
    </DataViewHeader>
    <DataViewContent
        v-model:selection="selectedItems"
        :show-bulk-select="true"
        :items="items"
        :loading="loading"
        blank-slate-text="No affected components found!"
        blank-slate-title="No Affected Components!"
        blank-slate-icon="fa fa-plug-circle-exclamation"
    >
        <template #item="{ item }">
            <div class="flex flex-1 items-center">
                <div class="flex-1">
                    {{ item.data }}
                </div>
                <div class="flex-shrink-0">
                    <!-- Prevent the select field from growing -->
                    <Select v-model="item.status" :options="findingComponentStatus()" @update:modelValue="patchComponent(item)"></Select>
                </div>
            </div>
        </template>
    </DataViewContent>
</template>
