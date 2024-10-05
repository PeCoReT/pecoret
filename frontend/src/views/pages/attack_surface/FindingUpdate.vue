<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import ASMonitorService from '@/service/ASMonitorService';
import InlineField from '@/components/common/forms/InlineField.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import SeveritySelectField from '@/components/forms/fields/SeveritySelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import CWEMultiSelectField from '@/components/forms/fields/CWEMultiSelectField.vue';
import forceFileDownload from '@/utils/file';
import AffectedComponentFindingCard from "@/components/cards/attack_surface/AffectedComponentFindingCard.vue";

export default {
    name: 'FindingUpdate',
    components: {AffectedComponentFindingCard, CWEMultiSelectField, MarkdownEditor, SeveritySelectField, InlineFieldGroup, InlineField, BaseLayout },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'AttackSurfaceFindingList'
                    })
                },
                {
                    label: 'Update',
                    disabled: true
                }
            ],
            service: new ASMonitorService(),
            model: {},
            findingId: this.$route.params.findingId,
            loaded: false,
            downloadLoading: false
        };
    },
    mounted() {
        this.getItem();
    },
    methods: {
        findingProgressStatus() {
            return this.service.getFindingProgressChoices();
        },
        getItem() {
            this.service.getFinding(this.findingId).then((response) => {
                this.model = response.data;
                this.loaded = true;
            });
        },
        downloadPDF() {
            this.downloadLoading = true;
            this.service
                .downloadFindingPDF(this.findingId)
                .then((response) => {
                    forceFileDownload(response);
                })
                .finally(() => {
                    this.downloadLoading = false;
                });
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this finding?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteFinding(this.findingId);
                    this.$router.push({ name: 'AttackSurfaceFindingList' });
                }
            });
        },
        save() {
            let data = {
                title: this.model.title,
                description: this.model.description,
                recommendation: this.model.recommendation,
                severity: this.model.severity,
                cwe_ids: this.model.cwe_ids,
                internal_notes: this.model.internal_notes,
                cvss_score: this.model.cvss_score,
                exploitation_details: this.model.exploitation_details,
                status: this.model.status
            };
            this.service.patchFinding(this.findingId, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Finding updated!',
                    life: 3000,
                    detail: 'Finding updated successfully!'
                });
            });
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #pre-content-right>
            <div class="flex justify-end">
                <Button icon="fa fa-download" @click="downloadPDF" :loading="downloadLoading" class="mr-3" label="Download"></Button>
                <Button outlined severity="danger" @click="confirmDialogDelete" label="Delete" icon="fa fa-trash"></Button>
            </div>
        </template>
        <div class="card col-span-12">
            <Form v-if="loaded">
                <Field label="Title">
                    <InputText v-model="model.title"></InputText>
                </Field>
                <InlineFieldGroup>
                    <InlineField label="Severity">
                        <SeveritySelectField v-model="model.severity"></SeveritySelectField>
                    </InlineField>
                    <InlineField label="Status">
                        <Select :options="findingProgressStatus()" optionLabel="name" optionValue="value" v-model="model.status"></Select>
                    </InlineField>
                </InlineFieldGroup>
                <Field label="CVSS-Score">
                    <InputText v-model="model.cvss_score"></InputText>
                </Field>
                <Field label="Description">
                    <MarkdownEditor v-model="model.description"></MarkdownEditor>
                </Field>
                <Field label="Exploitation Details">
                    <MarkdownEditor v-model="model.exploitation_details"></MarkdownEditor>
                </Field>
                <Field label="Recommendation">
                    <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
                </Field>
                <Field label="CWEs">
                    <CWEMultiSelectField v-model="model.cwe_ids"></CWEMultiSelectField>
                </Field>
                <Button label="Save" @click="save" class="w-full mt-3"></Button>
            </Form>
            <div v-else class="grid w-full">
                <Skeleton class="mb-2"></Skeleton>
                <Skeleton width="10rem" class="mb-2"></Skeleton>
                <Skeleton width="5rem" class="mb-2"></Skeleton>
                <Skeleton height="2rem" class="mb-2"></Skeleton>
                <Skeleton width="10rem" height="4rem"></Skeleton>
            </div>
        </div>
        <AffectedComponentFindingCard></AffectedComponentFindingCard>
    </BaseLayout>
</template>
