<script>
import { Badge } from '@/components/badge';
import { randomHexColor } from '@/lib/colors';
import LabelForm from '@/partials/advisories/LabelForm.vue';
import { BlankSlate } from '@/components/blankslate';
import { Button } from '@/components/ui/button';
import SearchField from '@/partials/common/SearchField.vue';
import { Paginator } from '@/components/paginator';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import { listViewMixin } from '@/mixins/listViewMixin';
import { paramMixin } from '@/mixins/params';

export default {
    name: 'TagList',
    components: {
        DataViewListLayout,
        DataViewContent,
        SearchField,
        Button,
        BlankSlate,
        LabelForm,
        Badge,
        Paginator
    },
    mixins: [listViewMixin, paramMixin],
    data() {
        return {
            loading: false,
            filters: { search: { value: null } },
            items: [],
            newTag: { color: randomHexColor() },
            hideCreateForm: true,
            showEditForm: null
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asTagList, null, data)
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
        create() {
            this.$api.post(this.$api.e.asTagList, null, this.newTag).then(() => {
                this.$toaster({
                    title: 'Tag created!',
                    duration: 3000,
                    description: 'Tag created successfully'
                });
                this.newLabel = { color: randomHexColor() };
                this.hideCreateForm = true;
                this.getItems();
            });
        },
        edit(label) {
            let data = { color: label.color, description: label.description, name: label.name };
            this.$api.patch(this.$api.e.asTagDetail, { pk: label.pk }, data).then(() => {
                this.getItems();
                this.showEditForm = null;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this tag?',
                accept: () => {
                    this.$api.delete(this.$api.e.asTagDetail, { pk: id }).then(() => {
                        this.$toaster({
                            title: 'Deleted',
                            description: 'Tag was removed!',
                            duration: 3000
                        });
                        this.showEditForm = null;
                        this.getItems();
                    });
                }
            });
        }
    }
};
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
                <i class="fa fa-plus"></i> Tag
            </Button>
        </template>
        <Card v-if="hideCreateForm === false" class="col-span-12">
            <div class="flex">
                <Badge :color="newTag.color" text="Preview"></Badge>
            </div>
            <LabelForm v-model="newTag" v-model:display="hideCreateForm" @save="create"></LabelForm>
        </Card>
        <div class="mt-3">
            <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-tags"
                blank-slate-text="No tags found!" blank-slate-title="No Tags!">
                <template #item="{ item, index }">
                    <div class="flex-1">
                        <div class="flex justify-between items-center">
                            <Badge :color="item.color" :text="item.name"></Badge>

                            <div class="flex">
                                {{ item.description }}
                            </div>
                            <div class="flex items-center space-x-4 text-sm">
                                <Button variant="outline" @click="
                                    () => {
                                        if (showEditForm === index) {
                                            this.showEditForm = null;
                                        } else {
                                            this.showEditForm = index;
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
                                @save="edit(this.items[index])" />
                        </div>
                    </div>
                </template>
            </DataViewContent>
        </div>

        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
