<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import ProgramSelectField from '@/components/forms/fields/ProgramSelectField.vue';
import {DataTypeChoices, InScopeChoices} from "@/utils/constants";

export default {
    name: 'TargetUpdateDialog',
    components: { ProgramSelectField, ModalDialog, MarkdownEditor },
    emits: ['object-updated'],
    props: {
        target: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.target,
            loading: false,
        };
    },
    watch: {
        target: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    methods: {
        InScopeChoices() {
            return InScopeChoices
        },
        DataTypeChoices() {
            return DataTypeChoices
        },
        open() {
            this.showDialog = true;
        },
        patch() {
            this.loading = true;
            let data = {
                description: this.model.description,
                data_type: this.model.data_type,
                scope: this.model.scope,
                data: this.model.data
            };
            this.$api.patch(this.$api.e.asTargetDetail, {pk: this.target.pk}, data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Target updated!',
                        life: 3000,
                        detail: 'Target updated successfully!'
                    });
                    this.$emit('object-updated');
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>
<template>
    <Button icon="fa fa-edit" size="small" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="Update Target" v-model="showDialog" @onSave="patch">
        <Form>
            <Field label="Data">
                <InputText v-model="model.data" id="data"></InputText>
            </Field>
            <Field label="Data Type">
                <Select :options="DataTypeChoices()" optionLabel="name" optionValue="value" v-model="model.data_type"></Select>
            </Field>
            <Field label="Program">
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </Field>
            <Field label="Scope">
                <Select :options="InScopeChoices()" optionLabel="name" optionValue="value" v-model="model.scope"></Select>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
