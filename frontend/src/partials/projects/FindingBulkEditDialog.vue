<script>
import { findingStatusChoices, severityChoices } from '@/utils/constants';
import ModalDialog from '@/components/dialog/ModalDialog.vue';
import { Button } from '@/components/ui/button';

export default {
    name: 'FindingBulkEditDialog',
    components: { ModalDialog, Button },
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
                await this.$api
                    .patch(
                        this.$api.e.pFindingDetail,
                        {
                            pPk: this.projectId,
                            pk: this.finding.pk
                        },
                        data
                    )
                    .then(() => {});
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
    <ModalDialog :loading="loading" header="Finding Bulk Edit" v-model="visible">
        <template #trigger>
            <Button v-if="findings.length > 0" class="mb-2 ml-2" icon="fa fa-edit" outlined @click="open"></Button>
            <div class="p-fluid formgrid grid">
                <div class="field col-12">
                    <label>Severity</label>
                    <Select v-model="fields.severity" :options="severityChoices()" class="w-full" optionLabel="label" optionValue="value" show-clear></Select>
                </div>
            </div>
            <div class="p-fluid formgrid grid">
                <div class="field col-12">
                    <label>Status</label>
                    <Select v-model="fields.status" :options="findingStatusChoices()" class="w-full" optionLabel="title" optionValue="value" show-clear></Select>
                </div>
            </div>
        </template>
    </ModalDialog>

</template>
