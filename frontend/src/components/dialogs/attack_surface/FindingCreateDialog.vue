<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ProgramSelectField from "@/components/forms/fields/ProgramSelectField.vue";

export default {
    name: 'ASFindingCreateDialog',
    components: {ProgramSelectField, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                title: null,
                program: null
            },
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.service.createFinding(this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Finding created!',
                    life: 3000,
                    detail: 'Finding created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Finding" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Finding" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Title">
                <InputText v-model="model.title"></InputText>
            </Field>
            <Field label="Program">
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </Field>
        </Form>
    </ModalDialog>
</template>
