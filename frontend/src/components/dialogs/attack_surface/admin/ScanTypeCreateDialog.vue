<script>
import {allowedObjectTypeChoices} from '@/utils/constants';
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'ScanTypeCreateDialog',
    components: { ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                description: null,
                can_run_manually: false,
                allowed_object_type: null,
                conditions: null,
                priority: 4,
                enabled: true
            },
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
        create() {
            let data = {
                name: this.model.name,
                description: this.model.description,
                can_run_manually: this.model.can_run_manually,
                conditions: this.model.conditions,
                allowed_object_type: this.model.allowed_object_type,
                priority: this.model.priority,
                enabled: this.model.enabled
            };
            this.$api.post(this.$api.e.asScanTypeList, null, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Scan Type created!',
                    life: 3000,
                    detail: 'SCan Type created successfully'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Scan Type" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="New Scan Type" v-model="showDialog" @onSave="create">
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
