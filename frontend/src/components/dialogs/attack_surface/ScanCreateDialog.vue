<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/common/ModalDialog.vue';
import ScanTypeSelectField from '@/components/forms/fields/ScanTypeSelectField.vue';

export default {
    name: 'ScanCreateDialog',
    components: { ModalDialog, ScanTypeSelectField },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                scan_type: null,
                scan_objects: []
            },
            asset_type: null,
            scanObjectChoices: [],
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        setObjectType() {
            this.asset_type = this.model.scan_type.allowed_object_type;
            this.searchObjectType();
        },
        searchObjectType(query) {
            let data = {};
            if (query) {
                data['search'] = query;
            }
            let method;
            if (this.asset_type === 'host') {
                method = this.service.getHosts;
            } else if (this.asset_type === 'service') {
                method = this.service.getServices;
            } else if (this.asset_type === 'target') {
                method = this.service.getTargets;
            } else if (this.asset_type === 'port') {
                method = this.service.getPorts;
            } else if (this.asset_type === 'url') {
                method = this.service.getURLs;
            } else {
                return null;
            }
            method(data)
                .then((response) => {
                    this.scanObjectChoices = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        create() {
            this.loading = true;
            let data = {
                name: this.model.name,
                scan_type: this.model.scan_type.pk,
                scan_objects: []
            };
            for (let i = 0; i < this.model.scan_objects.length; i++) {
                let obj = this.model.scan_objects[i];
                data['scan_objects'].push({ content_type: this.asset_type.toLowerCase(), object_id: obj });
            }
            this.service
                .createScan(data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Scan created!',
                        life: 3000,
                        detail: 'Scan created successfully!'
                    });
                    this.$emit('object-created');
                    this.showDialog = false;
                    this.model.scan_type = null;
                    this.model.scan_objects = [];
                    this.model.name = null;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Scan" outlined @click="open"></Button>
    <ModalDialog :loading="loading" header="New Scan" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name"></InputText>
            </Field>
            <Field label="Scan Type">
                <ScanTypeSelectField v-model="model.scan_type" @update:model-value="setObjectType"></ScanTypeSelectField>
            </Field>
            <Field label="Scan Objects">
                <MultiSelect v-model="model.scan_objects" :filter="true" @filter="searchObjectType" :disabled="!asset_type" :options="scanObjectChoices" optionLabel="display_name" optionValue="pk"></MultiSelect>
            </Field>
        </Form>
    </ModalDialog>
</template>
