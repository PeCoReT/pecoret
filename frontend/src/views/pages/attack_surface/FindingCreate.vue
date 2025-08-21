<script>
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ModelCombobox } from '@/components/combobox';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'FindingCreate',
    components: { ContainerLayout, ModelCombobox, Input, Button, PageHeader },
    data() {
        return {
            model: {
                program: null,
                title: null
            }
        };
    },
    methods: {
        create() {
            this.$api.post(this.$api.e.asFindingList, null, this.model).then((response) => {
                this.$toaster({
                    title: 'Finding created!',
                    duration: 3000,
                    detail: 'Finding created successfully!'
                });
                this.$router.push({ name: 'AttackSurfaceFindingUpdate', params: { findingId: response.data.pk } });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Create Finding</PageHeader>
        <Form>
            <Field label="Title">
                <Input v-model="model.title"></Input>
            </Field>
            <Field label="Program">
                <ModelCombobox v-model="model.program" :api-endpoint="this.$api.e.asProgramList" align="start" abel-field="name" value-field="pk" variant="form"> </ModelCombobox>
            </Field>
            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </ContainerLayout>
</template>
