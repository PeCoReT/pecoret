<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import {asFindingStatusChoices, severityChoices} from '@/utils/constants';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ScanFindingDetail',
    components: { MarkdownEditor, InfoCardWithForm, DetailCardWithIcon },
    data() {
        return {
            finding: {},
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
            return asFindingStatusChoices;
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
                    this.$api.delete(this.$api.e.asScanFindingDetail, { pk: this.findingId }).then(() => {
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
            this.$api.get(this.$api.e.asScanFindingDetail, { pk: this.findingId }).then((response) => {
                this.finding = response.data;
            });
        },
        patchFindingData(data) {
            this.$api.patch(this.$api.e.asScanFindingDetail, { pk: this.findingId }, data).then((response) => {
                this.finding = response.data;
                this.$toast.add({ severity: 'success', summary: 'Updated', detail: 'Finding updated!', life: 3000 });
            });
        }
    }
};
</script>

<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-6"></div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <div class="card">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Name" icon="fa-fingerprint" class="bg-surface-950" :text="finding.name + `(by ${finding.tool})`"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950 w-full" title="Status" icon="fa-bookmark">
                            <Select v-model="finding.status" :options="statusChoices" optionValue="value" @change="patchFindingData({ status: finding.status })" optionLabel="name" class="w-full"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950" title="Severity" icon="fa fa-shield-halved">
                            <Select v-model="finding.severity" :options="severityChoices()" optionLabel="label" @change="patchFindingData({ severity: finding.severity })" optionValue="value"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Component" icon="fa-crosshairs" class="bg-surface-950" :text="finding.affected_component"></DetailCardWithIcon>
                    </div>
                </div>
                <Form class="mt-3">
                    <Field label="Result">
                        <MarkdownEditor v-model="finding.result" @blur="patchFindingData({ result: finding.result })"></MarkdownEditor>
                    </Field>
                    <Field label="Full Output">
                        <MarkdownEditor v-model="finding.full_output" @blur="patchFindingData({ full_output: finding.full_output })"></MarkdownEditor>
                    </Field>
                    <Field label="Comment">
                        <MarkdownEditor v-model="finding.comment" @blur="patchFindingData({ comment: finding.comment })"></MarkdownEditor>
                    </Field>
                </Form>
            </div>
        </div>
    </div>
</template>
