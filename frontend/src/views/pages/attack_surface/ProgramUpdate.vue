<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { MarkdownEditor } from '@/components/editor';
import { Input } from '@/components/ui/input';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import {Button} from '@/components/ui/button';
import {PageHeader} from "@/components/typography";


export default {
    name: 'ProgramUpdate',
    components: {PageHeader, ContainerLayout, MarkdownEditor, BaseLayout, Input, Button },
    data() {
        return {
            model: {},
            loading: false,
            programId: this.$route.params.programId
        };
    },
    mounted() {
        this.$api.get(this.$api.e.asProgramDetail, { pk: this.programId }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        patch() {
            this.loading = true;
            let data = {
                name: this.model.name,
                description: this.model.description
            };
            this.$api.patch(this.$api.e.asProgramDetail, { pk: this.programId }, data).then(() => {
                this.$toaster({
                    title: 'Program updated!',
                    duration: 3000,
                    detail: 'Program updated successfully!'
                });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Update Program</PageHeader>

        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name"></Input>
            </Field>
            <Field label="Description">
                <MarkdownEditor id="description" v-model="model.description"></MarkdownEditor>
            </Field>
            <Button class="w-full" @click="patch">Save</Button>
        </Form>
    </ContainerLayout>
</template>
