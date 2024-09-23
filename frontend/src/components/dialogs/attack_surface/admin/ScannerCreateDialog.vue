<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/common/ModalDialog.vue';
import ScanTypeMultiSelectField from '@/components/forms/fields/ScanTypeMultiSelectField.vue';

export default {
    name: 'ScannerCreateDialog',
    components: { ScanTypeMultiSelectField, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                scan_types: null
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
            let data = {
                name: this.model.name,
                scan_types: this.model.scan_types
            };
            this.service.createScanner(data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Scanner created!',
                    life: 3000,
                    detail: 'Scanner created successfully'
                });
                this.$emit('object-created', response.data);
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Scanner" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="New Scanner" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name"></InputText>
            </Field>
            <Field label="Scan Types">
                <ScanTypeMultiSelectField v-model="model.scan_types"></ScanTypeMultiSelectField>
            </Field>
        </Form>
    </ModalDialog>
</template>
