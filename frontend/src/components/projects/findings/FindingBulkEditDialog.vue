<script>
import FindingService, { statusChoices } from '@/service/FindingService';
import { findingStatusChoices, severityChoices } from '@/utils/constants';

export default {
    name: 'FindingBulkEditDialog',
    emits: ['object-updated'],
    props: {
        findings: {
            required: true
        }
    },
    data() {
        return {
            visible: false,
            fields: {
                severity: null,
                status: null
            },
            loading: false,
            service: new FindingService(),
            projectId: this.$route.params.projectId
        };
    },
    methods: {
        findingStatusChoices() {
            return findingStatusChoices;
        },
        severityChoices() {
            return severityChoices;
        },
        statusChoices() {
            return statusChoices;
        },
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        async patch() {
            let data = {};
            for (let [key, value] of Object.entries(this.fields)) {
                if (value !== null && value !== undefined) {
                    data[key] = value;
                }
            }
            this.loading = true;
            for (let i = 0; i < this.findings.length; i++) {
                await this.service.patchFinding(this.$api, this.projectId, this.findings[i].pk, data).then(() => {});
            }
            this.loading = false;
            this.fields.severity = null;
            this.$emit('object-updated');
            this.visible = false;
        }
    }
};
</script>

<template>
    <Button v-if="findings.length > 0" icon="fa fa-edit" outlined class="mb-2 ml-2" @click="open"></Button>

    <Dialog header="Finding Bulk Edit" v-model:visible="visible" modal :style="{ width: '70vw' }" :closable="!this.loading">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label>Severity</label>
                <Dropdown show-clear v-model="fields.severity" :options="severityChoices()" optionValue="value" optionLabel="label" class="w-full"></Dropdown>
            </div>
        </div>
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label>Status</label>
                <Dropdown show-clear v-model="fields.status" :options="findingStatusChoices()" optionValue="value" optionLabel="title" class="w-full"></Dropdown>
            </div>
        </div>
        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined" :disabled="this.loading === true"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined" :loading="this.loading"></Button>
        </template>
    </Dialog>
</template>
