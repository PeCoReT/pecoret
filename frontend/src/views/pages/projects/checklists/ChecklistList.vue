<script>
import markdown from '@/utils/markdown';
import AssetSelectField from '@/components/forms/fields/AssetSelectField.vue';
import AssetChecklistCreateDialog from '@/components/dialogs/AssetChecklistCreateDialog.vue';
import BaseLayout from '@/layout/base/BaseLayout.vue';

export default {
    name: 'ChecklistList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            categories: [],
            checklistChoices: [],
            activeChecklist: null,
            searchChecklist: null,
            searchCategories: null,
            asset: null,
            activeItem: null,
            breadcrumbs: [
                {
                    label: 'Checklists',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        renderMarkdown(text) {
            return markdown.renderMarkdown(text);
        },
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
                params = {};
            }
            if (this.asset && this.asset.pk) {
                params[this.asset.type] = this.asset.pk;
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
                .then(() => {});
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
    components: { BaseLayout, AssetSelectField, AssetChecklistCreateDialog }
};
</script>
<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #pre-content-right>
            <div class="flex justify-end">
                <AssetChecklistCreateDialog @object-created="loadAssetChecklists"></AssetChecklistCreateDialog>
            </div>
        </template>

        <div class="col-span-12">
            <Form>
                <InlineFieldGroup>
                    <AssetSelectField v-model="asset" :displayInline="true" @update:model-value="onAssetChange"></AssetSelectField>
                </InlineFieldGroup>
            </Form>
        </div>
        <div class="flex card col-span-12 gap-3">
            <!-- Left Sidebar - Checklists -->
            <div class="w-full md:w-1/5 p-4 shadow-md overflow-y-auto border-r border-gray-700">
                <div class="flex justify-between">
                    <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Checklists</h2>
                    <Button label="Checklist" size="small" severity="danger" v-if="this.activeChecklist && this.activeChecklist.pk" icon="fa fa-trash" outlined @click="onDeleteDialogChecklist"></Button>
                </div>

                <!-- Search Bar for Checklists -->
                <div class="mb-4">
                    <Form>
                        <Field>
                            <InputText v-model="searchChecklist" placeholder="Search checklists" @update:modelValue="doChecklistSearch" :disabled="!this.asset"></InputText>
                        </Field>
                    </Form>
                </div>

                <ul>
                    <li v-for="checklist in checklistChoices" :key="checklist.pk" class="w-full text-left mb-2 bg-gray-100 dark:bg-gray-700 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md focus:outline-none">
                        <div class="flex items-center gap-3 p-2">
                            <button @click="loadAssetCategories(checklist)" class="w-full">
                                {{ checklist.name }}
                            </button>
                        </div>
                    </li>
                </ul>
            </div>

            <!-- Middle Section - Categories and Items -->
            <div class="block w-full md:w-2/5 p-4 shadow-md overflow-y-auto border-r border-gray-700">
                <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Categories</h2>

                <!-- Search Bar for Categories -->
                <div class="mb-4">
                    <Form>
                        <Field>
                            <InputText v-model="searchCategories" placeholder="Search categories" :disabled="!this.asset"></InputText>
                        </Field>
                    </Form>
                </div>

                <div>
                    <div class="mb-6" v-for="category in categories" :key="category.pk">
                        <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-gray-100">{{ category.name }} ({{ category.closed_items }}/{{ category.items.length }})</h3>
                        <ul>
                            <li v-for="item in category.items" class="w-full text-left mb-2 bg-gray-100 dark:bg-gray-700 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md focus:outline-none">
                                <div class="flex items-center gap-3 p-2">
                                    <Checkbox @change="onCheckboxChange($event, item, category)" :binary="true" v-model="item.checked"></Checkbox>
                                    <button
                                        class="w-full"
                                        @click="
                                            () => {
                                                this.activeItem = item;
                                            }
                                        "
                                    >
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
                <h2 class="text-xl font-semibold mb-8 text-gray-900 dark:text-gray-100">Item Preview</h2>
                <div id="item-preview" class="text-gray-700 dark:text-gray-300">
                    <p class="text-lg" v-if="activeItem === null">Click on a checklist item to see the preview here.</p>
                    <div class="markdown-block" v-else v-html="renderMarkdown(activeItem.description)"></div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
