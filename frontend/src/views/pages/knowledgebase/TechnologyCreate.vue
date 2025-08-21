<script>
import { MarkdownEditor } from '@/components/editor';
import { Input } from '@/components/ui/input';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'TechnologyCreate',
    components: { ContainerLayout, MultiModelCombobox, MarkdownEditor, Input, Button, PageHeader },
    data() {
        return {
            model: {
                name: null,
                description: null,
                cpe: null,
                homepage: null,
                source_code_url: null,
                vendor: null,
            },
            loading: false
        };
    },
    methods: {
        create() {
            this.$api.post(this.$api.e.technologyList, null, this.model).then(() => {
                this.$toaster({
                    title: 'Technology created!',
                    duration: 3000,
                    detail: 'Technology created successfully!'
                });
                this.$router.push({ name: 'TechnologyList' });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Create Technology</PageHeader>
        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name"></Input>
            </Field>
            <InlineFieldGroup>
                <InlineField label="CPE">
                    <Input id="cpe" v-model="model.cpe"></Input>
                </InlineField>
                <InlineField label="Homepage">
                    <Input v-model="model.homepage"></Input>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Vendor">
                <Input v-model="model.vendor"></Input>
            </Field>
            <Field label="Source Code URL">
                <Input v-model="model.source_code_url"></Input>
            </Field>
            <Field label="Description">
                <MarkdownEditor id="description" v-model="model.description"></MarkdownEditor>
            </Field>
            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </ContainerLayout>
</template>
