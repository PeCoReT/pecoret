<script>
import { MarkdownEditor } from '@/components/editor';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'ProgramCreate',
    components: { ContainerLayout, MarkdownEditor, Input, Label, Button },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Programs',
                    route: this.$router.resolve({ name: 'AttackSurfaceProgramList' })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            model: {
                name: null,
                description: null
            }
        };
    },
    methods: {
        create() {
            this.$api.post(this.$api.e.asProgramList, null, this.model).then(() => {
                this.$toaster({
                    title: 'Program created!',
                    duration: 3000,
                    detail: 'Program created successfully!'
                });
                this.$router.push({ name: 'AttackSurfaceProgramList' });
            });
        }
    }
};
</script>
<template>
    <ContainerLayout>
        <h2 class="text-2xl mb-3">Create Program</h2>
        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name"></Input>
            </Field>
            <Field label="Description">
                <MarkdownEditor id="description" v-model="model.description"></MarkdownEditor>
            </Field>
            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </ContainerLayout>
</template>
