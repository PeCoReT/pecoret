<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/common/ModalDialog.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import InlineField from '@/components/common/forms/InlineField.vue';
import { serviceProtocolChoices } from '@/utils/constants';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'TargetPortCreateDialog',
    components: { TechnologyMultiSelectField, InlineField, InlineFieldGroup, ModalDialog },
    emits: ['object-created'],
    props: {
        target: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: { protocol: 'TCP' },
            loading: false,
            service: new ASMonitorService()
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
        serviceProtocolChoices() {
            return serviceProtocolChoices;
        },
        open() {
            this.showDialog = true;
        },
        patch() {
            this.loading = true;
            let data = {
                target: this.target.pk,
                port: this.model.port,
                protocol: this.model.protocol,
                service: this.model.service,
                banner: this.model.banner,
                technologies: this.model.technologies
            };
            this.service
                .createPort(data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Target updated!',
                        life: 3000,
                        detail: 'Port created successfully!'
                    });
                    this.$emit('object-created');
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
    <Button icon="fa fa-plus" size="small" outlined @click="open" label="Port"></Button>
    <ModalDialog v-model:loading="loading" header="Create Port" v-model="showDialog" @onSave="patch">
        <Form>
            <Field label="Port Number">
                <InputNumber v-model="model.port" :use-grouping="false"></InputNumber>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Service">
                    <InputText v-model="model.service"></InputText>
                </InlineField>
                <InlineField label="Protocol">
                    <Select :options="serviceProtocolChoices()" optionLabel="label" optionValue="value" v-model="model.protocol"></Select>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Technologies">
                <TechnologyMultiSelectField v-model="model.technologies"></TechnologyMultiSelectField>
            </Field>
            <Field label="Banner">
                <Textarea v-model="model.banner"></Textarea>
            </Field>
        </Form>
    </ModalDialog>
</template>
