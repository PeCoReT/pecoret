<script>
import ChecklistService from '@/service/ChecklistService';
import ChecklistItemUpdate from '@/components/dialogs/ChecklistItemUpdate.vue';
import ChecklistItemCreate from '@/components/dialogs/ChecklistItemCreate.vue';
import markdown from '@/utils/markdown';

export default {
    name: 'CategoryDetail',
    components: { ChecklistItemCreate, ChecklistItemUpdate },
    data() {
        return {
            categoryId: this.$route.params.categoryId,
            service: new ChecklistService(),
            loading: false,
            model: {},
            breadcrumbs: [
                {
                    label: 'Checklists',
                    to: this.$router.resolve({
                        name: 'ChecklistList'
                    })
                },
                {
                    label: 'Categories',
                    to: this.$router.resolve({
                        name: 'ChecklistCategoryList'
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getCategory();
    },
    methods: {
        getCategory() {
            this.loading = true;
            this.service
                .getCategory(this.$api, this.categoryId)
                .then((response) => {
                    this.model = response.data;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        renderMarkdown(text) {
            return markdown.renderMarkdown(text);
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this category?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteCategory(this.$api, this.categoryId).then(() => {
                        this.$router.push({ name: 'ChecklistCategoryList' });
                    });
                }
            });
        },
        confirmDialogDeleteItem(itemId) {
            this.$confirm.require({
                message: 'Do you want to delete this item?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteItem(this.$api, itemId).then(() => {
                        this.getCategory();
                    });
                }
            });
        }
    }
};
</script>

<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-span-6 h-full">
            <div class="flex justify-end">
                <ChecklistItemCreate @object-created="getCategory"></ChecklistItemCreate>

                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <div class="card">
                <Form>
                    <InlineFieldGroup>
                        <InlineField label="Category ID">
                            <InputText v-model="model.category_id"></InputText>
                        </InlineField>
                        <InlineField label="Name">
                            <InputText v-model="model.name"></InputText>
                        </InlineField>
                    </InlineFieldGroup>
                </Form>

                <div class="grid mt-3 grid-cols-12">
                    <div class="col-span-12">
                        <Skeleton v-if="loading === true"></Skeleton>
                        <Accordion v-else>
                            <AccordionTab v-for="(item, index) in model.items" :key="index">
                                <template #header>
                                    <div class="col-span-10 m-1 p-1">
                                        <span class="white-space-nowrap">{{ item.name }}</span>
                                    </div>
                                </template>
                                <div class="grid grid-cols-12">
                                    <div class="col-span-10 p-2">
                                        <span v-html="renderMarkdown(item.description)"></span>
                                    </div>
                                    <div class="col-span-2 p-2">
                                        <div class="flex justify-end">
                                            <ChecklistItemUpdate :item="item"></ChecklistItemUpdate>
                                            <Button icon="fa fa-trash" outlined severity="danger" @click="confirmDialogDeleteItem(item.pk)"></Button>
                                        </div>
                                    </div>
                                </div>
                            </AccordionTab>
                        </Accordion>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
