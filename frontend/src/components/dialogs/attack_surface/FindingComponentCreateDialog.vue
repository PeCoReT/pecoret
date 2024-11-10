<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import ServiceSelectField from '@/components/forms/fields/ServiceSelectField.vue';

export default {
    name: 'ASFindingComponentCreateDialog',
    components: { ModalDialog, ServiceSelectField },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                finding: this.$route.params.findingId,
                component: null
            },
            loading: false,
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.$api.post(this.$api.e.asFindingComponentList, null, this.model).then(() => {
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
