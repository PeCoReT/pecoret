<script>
import ASMonitorService from '@/service/ASMonitorService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import { findingStatusChoices, severityChoices } from '@/utils/constants';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'FindingDetail',
    components: { MarkdownEditor, InfoCardWithForm, DetailCardWithIcon },
    data() {
        return {
            finding: { target: {}, cwe: {} },
            service: new ASMonitorService(),
            programId: this.$route.params.programId,
            findingId: this.$route.params.findingId,
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'ASMonitorFindingList',
                        params: {
                            programId: this.$route.params.programId
                        }
                    })
                },
                {
                    label: 'Finding Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getFinding();
    },
    methods: {
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this finding?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteFinding();
                }
            });
        },
        findingStatusChoices() {
            return findingStatusChoices;
        },
        severityChoices() {
            return severityChoices;
        },
        getFinding() {
            this.service.getFinding(this.$api, this.programId, this.findingId).then((response) => {
                this.finding = response.data;
            });
        },
        patchFindingData(data) {
            this.service.patchFinding(this.$api, this.programId, this.findingId, data).then((response) => {
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
                        <DetailCardWithIcon title="Name" icon="fa-fingerprint" class="surface-ground" :text="finding.name"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Status" icon="fa-bookmark">
                            <Dropdown v-model="finding.status" :options="findingStatusChoices()" optionValue="value" @change="patchFindingData({ status: finding.status })" optionLabel="title" class="w-full"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground" title="Severity" icon="fa fa-shield-halved">
                            <Dropdown v-model="finding.severity" :options="severityChoices()" optionLabel="label" @change="patchFindingData({ severity: finding.severity })" optionValue="value"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Target" icon="fa-crosshairs" class="surface-ground" :text="finding.target.name"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid formgrid p-fluid">
                    <div class="field col-12">
                        <label for="proof">Proof</label>
                        <MarkdownEditor v-model="finding.proof_text" @blur="patchFindingData({ proof_text: finding.proof_text })"></MarkdownEditor>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
