<script>
import { defineComponent } from 'vue';
import { Badge } from '@/components/badge';
import { randomHexColor } from '@/lib/colors';
import LabelForm from '@/partials/advisories/LabelForm.vue';
import { Paginator } from '@/components/paginator';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import { Button } from '@/components/ui/button';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { listViewMixin } from "@/mixins/listViewMixin";

export default defineComponent({
    name: 'LabelList',
    components: {
        DataViewContent,
        DataViewListLayout,
        SearchField,
        LabelForm,
        Badge,
        Paginator,
        Button
    },
    mixins: [listViewMixin],
    data() {
        return {
            loading: false,
            items: [],
            filters: { search: { value: null } },
            newLabel: { color: randomHexColor() },
            hideCreateForm: true,
            showEditForm: null
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this label?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                accept: () => {
                    this.$api.delete(this.$api.e.aLabelDetail, { pk: id }).then(() => {
                        this.$toaster({
                            title: 'Deleted',
                            description: 'Label was removed!',
                            duration: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        create() {
            this.$api.post(this.$api.e.aLabelList, null, this.newLabel).then(() => {
                this.$toaster({
                    title: 'Label created!',
                    duration: 3000,
                    description: 'New label was created successfully!'
                });
                this.getItems();
                this.newLabel = { color: randomHexColor() };
            });
        },
        editLabel(label) {
            let data = { color: label.color, description: label.description, name: label.name };
            this.$api.patch(this.$api.e.aLabelDetail, { pk: label.pk }, data).then(() => {
                this.getItems();
                this.showEditForm = null;
            });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.aLabelList, null, data)
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
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button :disabled="hideCreateForm === false" @click="
                () => {
                    this.hideCreateForm = false;
                }
            ">
                <i class="fa fa-plus"></i> Label
            </Button>
        </template>
        <Card v-if="hideCreateForm === false" class="col-span-12 mt-3">
            <div class="flex">
                <Badge :color="newLabel.color" text="Preview"></Badge>
            </div>
            <LabelForm v-model="newLabel" v-model:display="hideCreateForm" @save="create"></LabelForm>
        </Card>
        <div class="mt-3">
            <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-tags"
                blank-slate-text="No tags found!" blank-slate-title="No Tags!">
                <template #item="{ item, index }">
                    <div class="flex-1">
                        <!-- Left: Badge (Item Name) -->
                        <div class="flex justify-between items-center">
                            <Badge :color="item.color" :text="item.name"></Badge>

                            <div class="flex">
                                {{ item.description }}
                            </div>
                            <div class="flex items-center space-x-4 text-sm">
                                <Button variant="outline" @click="
                                    () => {
                                        if (showEditForm === index) {
                                            showEditForm = null;
                                        } else {
                                            showEditForm = index;
                                        }
                                    }
                                ">
                                    <i class="fa fa-edit" /> Edit
                                </Button>
                                <Button
                                    class="border-destructive text-destructive hover:text-foreground hover:bg-destructive"
                                    variant="outline" @click="confirmDialogDelete(item.pk)"><i class="fa fa-trash" />
                                    Delete
                                </Button>
                            </div>
                        </div>
                        <!-- Edit Form Section (Displayed only if `showEditForm === index`) -->
                        <div v-if="showEditForm === index" class="mt-2">
                            <!-- Label Form takes full width below the item -->
                            <LabelForm v-model="this.items[index]" v-model:display="showEditForm"
                                @save="editLabel(this.items[index])" />
                        </div>
                    </div>
                </template>
            </DataViewContent>
        </div>

        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
