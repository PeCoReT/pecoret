<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { Card } from '@/components/card';
import { Input } from '@/components/ui/input';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import {PageHeader} from "@/components/typography";

export default {
    name: 'ChecklistCreate',
    components: { ChecklistTabMenu, ContainerLayout, MultiModelCombobox, BaseLayout, Card, Input, Button, PageHeader },
    data() {
        return {
            model: {
                categories: []
            }
        };
    },
    methods: {
        save() {
            let data = {
                name: this.model.name,
                checklist_id: this.model.checklist_id,
                categories: Array.from(this.model.categories)
            };
            this.$api.post(this.$api.e.checklistList, null, data).then(() => {
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
        <PageHeader>Create Checklist</PageHeader>
        <Form>
            <Field label="Checklist ID">
                <Input id="id" v-model="model.checklist_id"></Input>
            </Field>
            <Field label="Name">
                <Input id="name" v-model="model.name"></Input>
            </Field>
            <Field label="Categories">
                <MultiModelCombobox title="" v-model="model.categories" :options-url="this.$api.e.checkCategoryList"></MultiModelCombobox>
            </Field>
            <Button class="w-full" @click="save">Save</Button>
        </Form>
    </ContainerLayout>
</template>
