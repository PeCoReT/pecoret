<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import InlineField from '@/components/common/forms/InlineField.vue';
import ASMonitorService from '@/service/ASMonitorService';
import { serviceProtocolChoices } from '@/utils/constants';

export default {
    name: 'PortUpdateDialog',
    components: { InlineField, TechnologyMultiSelectField, InlineFieldGroup, ModalDialog },
    emits: ['object-updated'],
    props: {
        port: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.port,
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        serviceProtocolChoices() {
            return serviceProtocolChoices;
        },
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                port: this.model.port,
                service: this.model.service,
                protocol: this.model.protocol,
                banner: this.model.banner,
                technologies: this.model.technologies
            };
            if (this.model.technologies.length > 0 && this.model.technologies[0].pk) {
                delete data.technologies;
            }
            this.service.patchPort(this.port.pk, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Port updated!',
                    life: 3000,
                    detail: 'Port updated successfully'
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
    <ModalDialog v-model:loading="loading" header="Update port" v-model="showDialog" @onSave="patch">
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
