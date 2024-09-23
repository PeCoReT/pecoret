<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/common/ModalDialog.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import TargetSelectField from '@/components/forms/fields/TargetSelectField.vue';
import PortSelectField from '@/components/forms/fields/PortSelectField.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'ASServiceCreateDialog',
    components: { TechnologyMultiSelectField, PortSelectField, TargetSelectField, InlineFieldGroup, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                port: null,
                target: null,
                banner: null,
                technologies: [],
                tags: [],
                cert_san: null,
                cert_expiry: null,
                cert_subject: null,
                cert_valid_from: null,
                cert_fingerprint: null,
                cert_public_key_info: null
            },
            portChoices: [],
            target_choiceS: [],
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.loading = true;
            let data = {
                port: this.model.port,
                technologies: this.model.technologies,
                banner: this.model.banner,
                target: this.model.target
            };
            this.service.createService(data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Service created!',
                    life: 3000,
                    detail: 'Service created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Scan" outlined @click="open"></Button>
    <ModalDialog :loading="loading" header="New Scan" v-model="showDialog" @onSave="create">
        <Form>
            <InlineFieldGroup>
                <InlineField label="Target">
                    <TargetSelectField v-model="model.target"></TargetSelectField>
                </InlineField>
                <InlineField label="Port">
                    <PortSelectField v-model="model.port" :target="model.target"></PortSelectField>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Technologies">
                <TechnologyMultiSelectField :model-value="model.technologies"></TechnologyMultiSelectField>
            </Field>
            <Field label="Banner">
                <Textarea v-model="model.banner"></Textarea>
            </Field>
        </Form>
    </ModalDialog>
</template>
