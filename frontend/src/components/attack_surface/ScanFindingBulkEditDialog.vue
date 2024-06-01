<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';

export default {
    name: 'ScanFindingBulkEditDialog',
    components: { ModalDialog },
    emits: ['object-updated'],
    props: {
        findings: {
            required: true
        },
    },
    data() {
        return {
            showDialog: false,
            fields: {
                severity: null,
                status: null
            },
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        async onSave() {
            let data = {};
            for (let [key, value] of Object.entries(this.fields)) {
                if (value !== null && value !== undefined) {
                    data[key] = value;
                }
            }
            this.loading = true;
            for (let i = 0; i < this.findings.length; i++) {
                await this.service.patchScanFinding(this.$api, this.findings[i].pk, data).then(() => {});
            }
            this.loading = false;
            this.fields.status = null;
            this.fields.severity = null;
            this.$emit('object-updated');
            this.showDialog = false;
        },
        open() {
            this.showDialog = true;
        }
    }
};
</script>

<template>
    <Button v-if="findings.length > 0" icon="fa fa-edit" outlined class="ml-2" @click="open"></Button>

    <ModalDialog :loading="loading" header="Bulk Edit Findings" v-model="showDialog" @onSave="onSave">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label>Severity</label>
                <Dropdown show-clear v-model="fields.severity" :options="service.getSeverityChoices()" optionValue="value" optionLabel="name" class="w-full"></Dropdown>
            </div>
            <div class="field col-12">
                <label>Status</label>
                <Dropdown show-clear v-model="fields.status" :options="service.getStatusChoices()" optionValue="value" optionLabel="name"></Dropdown>
            </div>
        </div>
    </ModalDialog>
</template>
