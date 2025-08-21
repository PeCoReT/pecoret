<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { SeveritySelectField } from '@/partials/common';
import { MarkdownEditor } from '@/components/editor';
import forceFileDownload from '@/utils/file';
import { useAuthStore } from '@/store/auth';
import { AffectedComponentFindingCard } from '@/partials/attack_surface';
import { asFindingProgressStatus, severityChoices } from '@/utils/constants';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/select';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { ReloadIcon } from '@radix-icons/vue';

export default {
    name: 'FindingUpdate',
    components: {
        ReloadIcon,
        ContainerLayout,
        DefaultSkeleton,
        MultiModelCombobox,
        AffectedComponentFindingCard,
        MarkdownEditor,
        SeveritySelectField,
        BaseLayout,
        Input,
        Button,
        Select
    },
    data() {
        return {
            model: {},
            findingId: this.$route.params.findingId,
            loaded: false,
            downloadLoading: false,
            authStore: useAuthStore()
        };
    },
    mounted() {
        this.getItem();
        this.$api.post(this.$api.e.asFindingLock, { pk: this.findingId }).then(() => {});
    },
    methods: {
        severityChoices() {
            return severityChoices;
        },
        findingProgressStatus() {
            return asFindingProgressStatus;
        },
        getItem() {
            this.$api.get(this.$api.e.asFindingDetail, { pk: this.findingId }).then((response) => {
                this.model = response.data;
                if (this.model.is_locked === true && this.model.locked_by.pk !== this.authStore.me.pk) {
                    this.$router.push({ name: 'AttackSurfaceFindingDetail', params: { findingId: this.findingId } });
                } else {
                    this.loaded = true;
                }
            });
        },
        downloadPDF() {
            this.downloadLoading = true;
            this.$api
                .get(this.$api.e.asFindingPdf, { pk: this.findingId }, null, { responseType: 'arraybuffer' })
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
                    this.$api.delete(this.$api.e.asFindingDetail, { pk: this.findingId });
                    this.$router.push({ name: 'AttackSurfaceFindingList' });
                }
            });
        },
        onAttachmentUpload(file, onSuccess) {
            let data = new FormData();
            data.append('image', file);
            this.$api.post(this.$api.e.asFindingImageList, {}, data).then((resp) => {
                onSuccess(resp.data.storage_link);
            });
        },
        unlock() {
            this.$api.post(this.$api.e.asFindingUnlock, { pk: this.findingId }).then(() => {
                this.$router.push({ name: 'AttackSurfaceFindingDetail', params: { findingId: this.findingId } });
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
            if (typeof this.model.cwe_ids === 'object' && this.model.cwe_ids.length > 0 && this.model.cwe_ids[0].pk) {
                delete data['cwe_ids'];
            }
            this.$api.patch(this.$api.e.asFindingDetail, { pk: this.findingId }, data).then(() => {
                this.$toaster({
                    title: 'Finding updated!',
                    duration: 3000,
                    description: 'Finding updated successfully!'
                });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <h2 class="text-2xl">Update Finding</h2>
        </template>
        <template #right-header>
            <Button :disabled="downloadLoading" class="mr-3" @click="downloadPDF">
                <ReloadIcon class="animate-spin" v-if="downloadLoading" />
                <i class="fa fa-download" v-else />
                Download
            </Button>
            <Button :disabled="downloadLoading" class="mr-3" variant="outline" @click="unlock"> <i class="fa fa-right-from-bracket" /> Exit</Button>
            <Button variant="destructive" @click="confirmDialogDelete"><i class="fa fa-trash"></i> Delete</Button>
        </template>
        <Form v-if="loaded">
            <Field label="Title">
                <Input v-model="model.title"></Input>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Severity">
                    <Select v-model="model.severity" :options="severityChoices()"></Select>
                </InlineField>
                <InlineField label="Status">
                    <Select v-model="model.status" :options="findingProgressStatus()"></Select>
                </InlineField>
            </InlineFieldGroup>
            <Field label="CVSS-Score">
                <Input v-model="model.cvss_score"></Input>
            </Field>
            <Field label="Internal Notes">
                <MarkdownEditor v-model="model.internal_notes"></MarkdownEditor>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
            <Field label="Exploitation Details">
                <MarkdownEditor v-model="model.exploitation_details" :show-upload-button="true" @upload="onAttachmentUpload"></MarkdownEditor>
            </Field>
            <Field label="Recommendation">
                <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
            </Field>
            <Field label="CWEs">
                <MultiModelCombobox variant="form" value-field="pk" v-model="model.cwe_ids" :options-url="this.$api.e.cweList" title=""></MultiModelCombobox>
            </Field>
            <Button class="w-full mt-3" @click="save">Save</Button>
        </Form>
        <div v-else class="grid w-full">
            <DefaultSkeleton></DefaultSkeleton>
        </div>
        <AffectedComponentFindingCard v-if="loaded"></AffectedComponentFindingCard>
    </ContainerLayout>
</template>
