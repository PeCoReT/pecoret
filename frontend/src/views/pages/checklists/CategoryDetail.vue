<script>
import ChecklistService from '@/service/ChecklistService';
import ChecklistItemUpdate from '@/components/dialogs/ChecklistItemUpdate.vue';
import ChecklistItemCreate from '@/components/dialogs/ChecklistItemCreate.vue';

export default {
    name: 'CategoryDetail',
    components: { ChecklistItemCreate, ChecklistItemUpdate },
    data() {
        return {
            categoryId: this.$route.params.categoryId,
            service: new ChecklistService(),
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
            this.service.getCategory(this.$api, this.categoryId).then((response) => {
                this.model = response.data;
            });
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
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6 h-full">
            <div class="flex justify-content-end">
                <ChecklistItemCreate @object-created="getCategory"></ChecklistItemCreate>

                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="grid formgrid p-fluid">
                    <div class="field md:col-6 col-12">
                        <label for="category_id">Category ID</label>
                        <InputText v-model="model.category_id"></InputText>
                    </div>
                    <div class="field md:col-6 col-12">
                        <label for="name">Name</label>
                        <InputText v-model="model.name"></InputText>
                    </div>
                </div>

                <div class="grid">
                    <div class="col-12">
                        <DataView :value="model.items">
                            <template #list="slotProps">
                                <div v-for="(item, index) in slotProps.items" :key="index">
                                    <div class="card hover:surface-hover">
                                        <div class="grid">
                                            <div class="col-6">
                                                {{ item.name }}
                                            </div>
                                            <div class="col-6 flex justify-content-end">
                                                <ChecklistItemUpdate :item="item"></ChecklistItemUpdate>
                                                <Button icon="fa fa-trash" outlined severity="danger" @click="confirmDialogDeleteItem(item.pk)"></Button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </DataView>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>