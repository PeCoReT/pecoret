<script>
import ChecklistService from '@/service/ChecklistService';
import markdown from '@/utils/markdown';
import AssetSelectField from '@/components/forms/fields/AssetSelectField.vue';
import AssetChecklistCreateDialog from '@/components/dialogs/AssetChecklistCreateDialog.vue';

export default {
    name: 'ChecklistList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            categories: [],
            selectedKey: null,
            checklistChoices: [],
            checklist: null,
            expandedItem: null,
            service: new ChecklistService(),
            asset: null,
            model: null,
            breadcrumbs: [
                {
                    label: 'Checklists',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        getChecklists() {
            this.service.getChecklists(this.$api).then((response) => {
                this.checklistChoices = response.data.results;
            });
        },
        renderMarkdown(text) {
            return markdown.renderMarkdown(text);
        },
        onAssetChange() {
            this.loadAssetChecklists();
        },
        onChecklistChange() {
            this.loadAssetCategories();
        },
        loadAssetCategories(event) {
            let params = {
                checklist: this.checklist
            };
            if (event) {
                params['search'] = event;
            }
            this.service.getAssetCategories(this.$api, this.projectId, params).then((response) => {
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
        loadAssetChecklists() {
            let params = {};
            params[this.asset.type] = this.asset.pk;
            this.service.getAssetChecklists(this.$api, this.projectId, params).then((response) => {
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
            return this.service.patchAssetItem(this.$api, this.projectId, item.pk, data).then(() => {});
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
                    this.service.deleteAssetChecklist(this.$api, this.projectId, this.checklist).then((response) => {
                        this.model = null;
                        this.checklist = null;
                        this.asset = null;
                        this.expandedItem = null;
                        this.categories = [];
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
    mounted() {},
    components: { AssetSelectField, AssetChecklistCreateDialog }
};
</script>
<template>
    <div class="grid mt-3">
        <pBreadcrumb v-model="breadcrumbs" />
    </div>
    <div class="grid mt-3 grid-cols-2">
        <div class="col-span-1"></div>
        <div class="col-span-1">
            <div class="flex justify-end">
                <AssetChecklistCreateDialog @object-created="getChecklists"></AssetChecklistCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-1">
        <div class="col-span-1">
            <div class="card">
                <Form>
                    <InlineFieldGroup>
                        <AssetSelectField v-model="asset" :displayInline="true" @update:model-value="onAssetChange"></AssetSelectField>
                        <InlineField label="Checklist">
                            <Select :options="checklistChoices" placeholder="Checklist" v-model="checklist" @change="onChecklistChange" :disabled="checklistChoices.length < 1" optionLabel="name" optionValue="pk"></Select>
                        </InlineField>
                    </InlineFieldGroup>
                </Form>
                <div class="grid mt-3 grid-cols-1 md:grid-cols-2">
                    <div class="col-span-1">
                        <div class="flex justify-between flex-column sm:flex-row">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </div>
                    <div class="col-span-1">
                        <div class="flex justify-end">
                            <Button label="Checklist" severity="danger" :disabled="this.checklist === null" icon="fa fa-trash" outlined @click="onDeleteDialogChecklist"></Button>
                        </div>
                    </div>
                </div>
                <div class="grid grid-cols-2 mt-3">
                    <Accordion class="mt-3 w-full col-span-1">
                        <AccordionPanel v-for="category in categories" :key="category.pk">
                            <AccordionHeader>{{ category.name }} ({{ category.closed_items }}/{{ category.items.length }}) </AccordionHeader>
                            <AccordionContent>
                                <div class="grid grid-cols-1">
                                    <div class="col-span-1">
                                        <div class="flex items-center" v-for="item in category.items">
                                                <Checkbox @change="onCheckboxChange($event, item, category)" :binary="true" v-model="item.checked"></Checkbox>
                                                <label class="ml-3">
                                                    <Button @click="this.expandedItem = item" :text="true" class="text-color">
                                                        {{ item.name }}
                                                    </Button>
                                                </label>
                                        </div>
                                    </div>
                                </div>
                            </AccordionContent>
                        </AccordionPanel>
                    </Accordion>
                    <div class="col-span-1 h-full" v-if="expandedItem">
                        <div class="card surface-ground">
                            <div v-html="renderMarkdown(expandedItem.description)" class="checklist-description"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
