<script>
import ChecklistService from '@/service/ChecklistService';

export default {
    name: 'ChecklistCreate',
    data() {
        return {
            model: {
                categories: null
            },
            categoryChoices: [],
            service: new ChecklistService(),
            searchAvailable: null,
            breadcrumbs: [
                {
                    label: 'Checklists',
                    to: this.$router.resolve({
                        name: 'ChecklistList'
                    })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.service.getCategories(this.$api).then((response) => {
            this.categoryChoices = [response.data.results, []];
        });
    },
    methods: {
        searchCategories() {
            let data = {
                search: this.searchAvailable
            };
            this.service.getCategories(this.$api, data).then((response) => {
                this.categoryChoices = [response.data.results, []];
            });
        },
        save() {
            let data = {
                name: this.model.name,
                checklist_id: this.model.checklist_id,
                categories: []
            };
            if (this.categoryChoices.length === 2) {
                this.categoryChoices[1].forEach((item) => {
                    data.categories.push(item.pk);
                });
            }
            this.service.createChecklist(this.$api, data).then(() => {
                this.$router.push({
                    name: 'ChecklistList'
                });
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
        <div class="col-12">
            <div class="card">
                <div class="grid formgrid p-fluid">
                    <div class="field col-12">
                        <label for="id">Checklist ID</label>
                        <InputText id="id" v-model="model.checklist_id"></InputText>
                    </div>
                    <div class="field col-12">
                        <label for="name">Name</label>
                        <InputText id="name" v-model="model.name"></InputText>
                    </div>

                    <div class="col-12 field">
                        <label for="categories">Categories</label>
                        <PickList id="categories" v-model="categoryChoices" :show-source-controls="false" :show-target-controls="false" listStyle="height:342px" dataKey="pk" breakpoint="1400px">
                            <template #sourceheader>
                                Available
                                <span class="p-input-icon-left mt-3">
                                    <i class="pi pi-search" />
                                    <InputText :disabled="categoryChoices.length < 2 || categoryChoices[0].length === 0" v-model="searchAvailable" placeholder="Search" @update:model-value="searchCategories" />
                                </span>
                            </template>
                            <template #targetheader>
                                Selected
                                <span class="p-input-icon-left mt-3">
                                    <i class="pi pi-search" />
                                    <InputText :disabled="true" v-model="searchAvailable" placeholder="Search" @change="searchCategories"></InputText>
                                </span>
                            </template>
                            <template #item="slotProps">
                                <div class="flex flex-wrap p-2 align-items-center gap-3">
                                    <div class="flex-1 flex flex-column gap-2">
                                        <span class="font-bold">{{ slotProps.item.name }}</span>
                                        <div class="flex align-items-center gap-2">
                                            <span>{{ slotProps.item.category_id }}</span>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </PickList>
                    </div>
                    <div class="col-12 mt-3">
                        <Button label="Save" @click="save"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>