<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import {allowedObjectTypeChoices} from '@/utils/constants';

export default {
    name: 'ScanTypeUpdateDialog',
    components: { ModalDialog },
    emits: ['object-updated'],
    props: {
        scanType: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.scanType,
            loading: false,
        };
    },
    methods: {
        allowedObjectTypeChoices() {
            return allowedObjectTypeChoices;
        },
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description,
                allowed_object_type: this.model.allowed_object_type,
                can_run_manually: this.model.can_run_manually,
                conditions: this.model.conditions,
                priority: this.model.priority,
                enabled: this.model.enabled
            };
            this.$api.patch(this.$api.e.asScanTypeDetail, { pk: this.scanType.pk }, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Scan Type updated!',
                    life: 3000,
                    detail: 'Scan type updated successfully'
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
    <ModalDialog v-model:loading="loading" header="Update Scan Type" v-model="showDialog" @onSave="patch">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name"></InputText>
            </Field>
            <Field label="Allowed Object Type">
                <Select :options="allowedObjectTypeChoices()" optionLabel="label" optionValue="value" v-model="model.allowed_object_type"></Select>
            </Field>
            <Field label="Priority">
                <InputNumber v-model="model.priority"></InputNumber>
                <small>Higher priority will be queued last</small>
            </Field>
            <Field label="Can Run Manually?">
                <ToggleSwitch v-model="model.can_run_manually"></ToggleSwitch>
            </Field>
            <Field label="Enabled?">
                <ToggleSwitch v-model="model.enabled"></ToggleSwitch>
            </Field>
            <Field label="Description">
                <Textarea v-model="model.description"></Textarea>
            </Field>
        </Form>
    </ModalDialog>
</template>
