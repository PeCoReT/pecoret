<script>
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
                await this.$api.patch(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.finding.pk }, data).then(() => {});
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
                <Select show-clear v-model="fields.severity" :options="severityChoices()" optionValue="value" optionLabel="label" class="w-full"></Select>
            </div>
        </div>
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label>Status</label>
                <Select show-clear v-model="fields.status" :options="findingStatusChoices()" optionValue="value" optionLabel="title" class="w-full"></Select>
            </div>
        </div>
        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined" :disabled="this.loading === true"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined" :loading="this.loading"></Button>
        </template>
    </Dialog>
</template>
