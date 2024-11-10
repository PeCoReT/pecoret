<script>

export default {
    name: 'ChecklistUpdate',
    data() {
        return {
            model: {
                categories: null
            },
            categoryChoices: [],
            checklistId: this.$route.params.checklistId,
            searchAvailable: null,
            breadcrumbs: [
                {
                    label: 'Checklists',
                    to: this.$router.resolve({
                        name: 'ChecklistList'
                    })
                },
                {
                    label: 'Update',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.$api.get(this.$api.e.checkCategoryList).then((response) => {
            this.categoryChoices = [response.data.results, []];
            this.$api.get(this.$api.e.checklistDetail, { pk: this.checklistId }).then((response) => {
                this.categoryChoices[1] = response.data.categories;
                this.model.name = response.data.name;
                this.model.checklist_id = response.data.checklist_id;
                response.data.categories.forEach((item) => {
                    for (let i = 0; i < this.categoryChoices[0].length; i++) {
                        if (this.categoryChoices[0][i].pk === item.pk) {
                            this.categoryChoices[0].splice(i, 1);
                        }
                    }
                });
            });
        });
    },
    methods: {
        searchCategories() {
            let data = {
                search: this.searchAvailable
            };
            this.$api.get(this.$api.e.checkCategoryList, null, data).then((response) => {
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
            this.$api.patch(this.$api.e.checklistDetail, { pk: this.checklistId }, data).then(() => {
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
                    <Button label="Save" @click="save" class="w-full"></Button>
                </Form>
            </div>
        </div>
    </div>
</template>
