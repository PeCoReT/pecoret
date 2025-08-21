<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { Card } from '@/components/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import {PageHeader} from "@/components/typography";

export default {
    name: 'ChecklistUpdate',
    components: { ChecklistTabMenu, ContainerLayout, MultiModelCombobox, Input, BaseLayout, Card, Button, PageHeader },
    data() {
        return {
            model: {
                categories: []
            },
            checklistId: this.$route.params.checklistId
        };
    },
    mounted() {
        this.$api.get(this.$api.e.checklistDetail, { pk: this.checklistId }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        save() {
            let data = {
                name: this.model.name,
                checklist_id: this.model.checklist_id,
                categories: Array.from(this.model.categories)
            };
            if (data.categories && data.categories.length > 0 && data.categories[0].pk) {
                delete data.categories;
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
    <ContainerLayout>
        <template #left-header>
            <ChecklistTabMenu class="md:max-w-lg"></ChecklistTabMenu>
        </template>
        <PageHeader>Update Checklist</PageHeader>
        <Form>
            <Field label="Checklist ID">
                <Input id="id" v-model="model.checklist_id"></Input>
            </Field>
            <Field label="Name">
                <Input id="name" v-model="model.name"></Input>
            </Field>
            <Field label="Categories">
                <MultiModelCombobox title="" v-model="model.categories" :options-url="this.$api.e.checkCategoryList" label-field="category_id"></MultiModelCombobox>
            </Field>
            <Button class="w-full" @click="save">Save</Button>
        </Form>
    </ContainerLayout>
</template>
