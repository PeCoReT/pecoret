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

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <div class="card">
                <Form>
                    <Field label="Checklist ID">
                        <InputText id="id" v-model="model.checklist_id"></InputText>
                    </Field>
                    <Field label="Name">
                        <InputText id="name" v-model="model.name"></InputText>
                    </Field>
                    <Field label="Categories">
                        <PickList id="categories" v-model="categoryChoices" :show-source-controls="false" :show-target-controls="false" listStyle="height:342px" dataKey="pk" breakpoint="1400px">
                            <template #sourceheader>
                                <div class="flex flex-row align-center">
                                    <p class="flex text-xl">Available</p>
                                    <div class="justify-end flex flex-grow">
                                        <IconField iconPosition="left">
                                            <InputIcon class="fa fa-search"></InputIcon>
                                            <InputText :disabled="categoryChoices.length < 2 || categoryChoices[0].length === 0" v-model="searchAvailable" placeholder="Search" @update:model-value="searchCategories" />
                                        </IconField>
                                    </div>
                                </div>
                            </template>
                            <template #targetheader>
                                <div class="flex flex-row align-center">
                                    <p class="flex text-xl">Selected</p>
                                    <div class="justify-end flex flex-grow">
                                        <IconField iconPosition="left">
                                            <InputIcon class="fa fa-search"></InputIcon>
                                            <InputText :disabled="true" v-model="searchAvailable" placeholder="Search" @change="searchCategories"></InputText>
                                        </IconField>
                                    </div>
                                </div>
                            </template>
                            <template #item="slotProps">
                                <div class="flex flex-wrap align-center gap-2">
                                    <div class="flex-1 flex flex-col gap-1">
                                        <span class="font-bold">{{ slotProps.item.name }}</span>
                                        <div class="flex align-center gap-1">
                                            <span>{{ slotProps.item.category_id }}</span>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </PickList>
                    </Field>
                    <Button label="Save" class="w-full" @click="save"></Button>
                </Form>
            </div>
        </div>
    </div>
</template>
