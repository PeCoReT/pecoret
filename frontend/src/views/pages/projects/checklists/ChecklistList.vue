<script>
import renderMarkdown from '@/lib/markdown';
import { AssetChecklistCreateDialog, AssetSelectField } from '@/partials/projects';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Button } from '@/components/ui/button';
import SearchField from '@/partials/common/SearchField.vue';

export default {
    name: 'ChecklistList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            categories: [],
            filters: {
                search: { value: null },
            },
            checklistChoices: [],
            activeChecklist: null,
            searchChecklist: null,
            searchCategories: null,
            asset: null,
            activeItem: null
        };
    },
    methods: {
        renderMarkdown,
        doChecklistSearch(event) {
            this.loadAssetChecklists({ search: event });
        },
        onAssetChange() {
            this.loadAssetChecklists();
        },
        loadAssetCategories(checklist) {
            let params = {
                checklist: checklist.pk
            };
            this.activeChecklist = checklist;
            this.$api.get(this.$api.e.pCheckCategoryList, { projectPk: this.projectId }, params).then((response) => {
                this.categories = response.data.results;
                this.categories.forEach((category) => {
                    category.children = category.items;
                    category.closed_items = 0;
                    category.key = category.pk.toString();
                    category.children.forEach((item) => {
                        item.checked = false;
                        if (item.status === 'Closed') {
                            item.checked = true;
                            category.closed_items += 1;
                        }
                    });
                });
            });
        },
        loadAssetChecklists(params) {
            if (!params) {
                params = { asset: this.asset };
            }
            if (!this.asset) {
                this.checklistChoices = [];
                return;
            }
            if (this.asset && this.asset.pk) {
                params['asset'] = this.asset.pk;
            }
            this.$api.get(this.$api.e.pChecklistList, { projectPk: this.projectId }, params).then((response) => {
                this.checklistChoices = response.data.results;
            });
        },
        onCheckboxChange(event, item, category) {
            let status = 'Open';
            if (item.checked === true) {
                status = 'Closed';
                category.closed_items += 1;
            } else {
                category.closed_items -= 1;
            }
            let data = {
                status: status
            };
            return this.$api
                .patch(
                    this.$api.e.pCheckItemDetail,
                    {
                        projectPk: this.projectId,
                        pk: item.pk
                    },
                    data
                )
                .then(() => { });
        },
        onGlobalSearch(event) {
            this.loadAssetCategories(event);
        },
        onDeleteDialogChecklist() {
            this.$confirm.require({
                message: 'Do you want to delete this checklist for the asset?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api
                        .delete(this.$api.e.pChecklistDetail, {
                            projectPk: this.projectId,
                            pk: this.activeChecklist.pk
                        })
                        .then(() => {
                            this.activeChecklist = null;
                            this.asset = null;
                            this.categories = [];
                            this.loadAssetChecklists();
                            this.$router.push({
                                name: 'ProjectChecklistList',
                                params: {
                                    projectId: this.projectId
                                }
                            });
                        });
                }
            });
        }
    },
    components: {
        SearchField,
        ModelCombobox,
        Input,
        BaseLayout,
        AssetSelectField,
        AssetChecklistCreateDialog,
        Checkbox,
        Button
    }
};
</script>
<template>
    <BaseLayout>
        <template #pre-content-left>
            <ModelCombobox variant="form" v-model="asset" label="Select asset" :api-endpoint="this.$api.e.pAssetList"
                :url-args="{ pPk: projectId }" @update:model-value="onAssetChange" :fluid="true" align="start">
            </ModelCombobox>
        </template>
        <template #pre-content-right>
            <div class="flex justify-end">
                <AssetChecklistCreateDialog @object-created="loadAssetChecklists"></AssetChecklistCreateDialog>
            </div>
        </template>

        <div class="flex card col-span-12 gap-3">
            <!-- Left Sidebar - Checklists -->
            <div class="w-full md:w-1/5 p-4 shadow-md overflow-y-auto border-r border-input">
                <div class="flex justify-between">
                    <h2 class="text-xl font-semibold">Checklists</h2>
                    <Button v-if="this.activeChecklist && this.activeChecklist.pk" variant="destructive"
                        @click="onDeleteDialogChecklist"><i class="fa fa-trash"></i> Delete </Button>
                </div>

                <!-- Search Bar for Checklists -->
                <div class="mb-4">
                    <Form>
                        <Field>
                            <SearchField v-model="filters.search.value" @search="doChecklistSearch"
                                placeholder="Search checklists" :disabled="!this.asset"></SearchField>
                        </Field>
                    </Form>
                </div>

                <ul>
                    <li v-for="checklist in checklistChoices" :key="checklist.pk"
                        class="w-full mb-2 border rounded-md items-center gap-3 p-2"
                        :class="activeChecklist && checklist.pk === activeChecklist.pk ? 'bg-muted text-muted-foreground' : 'hover:text-accent-foreground hover:bg-accent hover hover:cursor-pointer '">
                        <button class="w-full" @click="loadAssetCategories(checklist)"
                            :disabled="activeChecklist && checklist.pk === activeChecklist.pk">
                            {{ checklist.name }}
                        </button>
                    </li>
                </ul>
            </div>

            <!-- Middle Section - Categories and Items -->
            <div class="block w-full md:w-2/5 p-4 shadow-md overflow-y-auto border-r border-input">
                <h2 class="text-xl font-semibold mb-4">Categories</h2>

                <!-- Search Bar for Categories -->
                <div class="mb-4">
                    <Form>
                        <Field>
                            <SearchField v-model="searchCategories" :disabled="true" placeholder="Search categories">
                            </SearchField>
                        </Field>
                    </Form>
                </div>

                <div>
                    <div v-for="category in categories" :key="category.pk" class="mb-6">
                        <h3 class="text-lg font-semibold mb-2">{{ category.name }} ({{ category.closed_items }}/{{
                            category.items.length }})</h3>
                        <ul>
                            <li v-for="item in category.items"
                                class="w-full text-left mb-2 rounded-md border hover:bg-accent hover:text-accent-foreground"
                                :class="item.checked ? 'bg-muted text-muted-foreground' : 'hover:text-accent-foreground hover:bg-accent hover hover:cursor-pointer '">
                                <div class="flex items-center gap-3 p-2">
                                    <Checkbox v-model:checked="item.checked"
                                        @update:checked="onCheckboxChange($event, item, category)"></Checkbox>
                                    <button class="w-full" @click="
                                        () => {
                                            this.activeItem = item;
                                        }
                                    ">
                                        {{ item.name }}
                                    </button>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Right Sidebar - Item Preview -->
            <div class="block w-full md:w-2/5 shadow-md overflow-y-auto">
                <h2 class="text-xl font-semibold mb-8">Item Preview</h2>
                <div id="item-preview">
                    <p v-if="activeItem === null" class="text-base">Click on a checklist item to see the preview here.
                    </p>
                    <div v-else class="markdown-block text-base" v-html="renderMarkdown(activeItem.description)"></div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
