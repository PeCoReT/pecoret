<script>
import { MarkdownEditor } from '@/components/editor';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'TechnologyUpdate.vue',
    components: { ContainerLayout, MultiModelCombobox, MarkdownEditor, Button, Input, PageHeader },
    data() {
        return {
            pk: this.$route.params.techId,
            model: {}
        };
    },
    mounted() {
        this.$api.get(this.$api.e.technologyDetail, { pk: this.pk }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description,
                cpe: this.model.cpe,
                homepage: this.model.homepage,
                source_code_url: this.model.source_code_url,
                vendor: this.model.vendor
            };
            this.$api.patch(this.$api.e.technologyDetail, { pk: this.pk }, data).then(() => {
                this.$toaster({
                    title: 'Technology updated!',
                    duration: 3000,
                    detail: 'Technology updated successfully!'
                });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Update Technology</PageHeader>
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
            <Button class="w-full" @click="patch">Save</Button>
        </Form>
    </ContainerLayout>
</template>
