<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ProgramSelectField from "@/components/forms/fields/ProgramSelectField.vue";
import ServiceSelectField from "@/components/forms/fields/ServiceSelectField.vue";

export default {
    name: 'ASFindingComponentCreateDialog',
    components: {ModalDialog, ServiceSelectField },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                finding: this.$route.params.findingId,
                component: null
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
            this.service.createFindingComponent(this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Component created!',
                    life: 3000,
                    detail: 'Component created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Component" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Component" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Service">
                <ServiceSelectField v-model="model.component"></ServiceSelectField>
            </Field>
        </Form>
    </ModalDialog>
</template>
