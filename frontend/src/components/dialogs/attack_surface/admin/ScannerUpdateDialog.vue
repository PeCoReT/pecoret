<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import ScanTypeMultiSelectField from '@/components/forms/fields/ScanTypeMultiSelectField.vue';

export default {
    name: 'ScannerUpdateDialog',
    components: { ScanTypeMultiSelectField, ModalDialog },
    emits: ['object-updated'],
    props: {
        scanner: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.scanner,
            loading: false,
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                scan_types: this.model.scan_types
            };
            if (this.model.scan_types.length > 0 && this.model.scan_types[0].pk) {
                delete data.scan_types;
            }
            this.$api.patch(this.$api.e.asScannerDetail, { pk: this.scanner.pk }, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Scanner updated!',
                    life: 3000,
                    detail: 'Scanner updated successfully'
                });
                this.$emit('object-updated');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" size="small" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="Update Scanner" v-model="showDialog" @onSave="patch">
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
