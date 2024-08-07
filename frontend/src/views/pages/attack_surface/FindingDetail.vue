<script>
import ASMonitorService from '@/service/ASMonitorService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import { severityChoices } from '@/utils/constants';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ScanFindingDetail',
    components: { MarkdownEditor, InfoCardWithForm, DetailCardWithIcon },
    data() {
        return {
            finding: {},
            service: new ASMonitorService(),
            findingId: this.$route.params.findingId,
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'AttackSurfaceScanFindingList'
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getFinding();
    },
    computed: {
        statusChoices() {
            return this.service.getStatusChoices();
        }
    },
    methods: {
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this finding?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteScanFinding(this.$api, this.findingId).then(() => {
                        this.$router.push({
                            name: 'AttackSurfaceScanFindingList'
                        });
                    });
                }
            });
        },
        severityChoices() {
            return severityChoices;
        },
        getFinding() {
            this.service.getScanFinding(this.$api, this.findingId).then((response) => {
                this.finding = response.data;
            });
        },
        patchFindingData(data) {
            this.service.patchScanFinding(this.$api, this.findingId, data).then((response) => {
                this.finding = response.data;
                this.$toast.add({ severity: 'success', summary: 'Updated', detail: 'Finding updated!', life: 3000 });
            });
        }
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Name" icon="fa-fingerprint" class="surface-ground" :text="finding.name + `(by ${finding.tool})`"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Status" icon="fa-bookmark">
                            <Dropdown v-model="finding.status" :options="statusChoices" optionValue="value" @change="patchFindingData({ status: finding.status })" optionLabel="name" class="w-full"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground" title="Severity" icon="fa fa-shield-halved">
                            <Dropdown v-model="finding.severity" :options="severityChoices()" optionLabel="label" @change="patchFindingData({ severity: finding.severity })" optionValue="value"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Component" icon="fa-crosshairs" class="surface-ground" :text="finding.affected_component"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid formgrid p-fluid">
                    <div class="field col-12">
                        <label for="description">Result</label>
                        <MarkdownEditor v-model="finding.result" @blur="patchFindingData({ result: finding.result })"></MarkdownEditor>
                    </div>
                    <div class="field col-12">
                        <label for="proof">Full Output</label>
                        <MarkdownEditor v-model="finding.full_output" @blur="patchFindingData({ full_output: finding.full_output })"></MarkdownEditor>
                    </div>
                    <div class="field col-12">
                        <label for="recommendation">Comment</label>
                        <MarkdownEditor v-model="finding.comment" @blur="patchFindingData({ comment: finding.comment })"></MarkdownEditor>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
