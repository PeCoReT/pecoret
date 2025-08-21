<script>
import { useAuthStore } from '@/store/auth';
import { Card } from '@/components/card';
import { Switch } from '@/components/ui/switch';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ReloadIcon } from '@radix-icons/vue';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import PageHeader from '@/components/typography/PageHeader.vue';
import BackLinkButton from '@/components/button/BackLinkButton.vue';
import { MarkdownEditor } from '@/components/editor';
import Field from '@/components/form/Field.vue';
import InlineField from '@/components/form/InlineField.vue';
import InlineFieldGroup from '@/components/form/InlineFieldGroup.vue';

export default {
    name: 'AdvisoryUpdate',
    data() {
        return {
            advisoryId: this.$route.params.advisoryId,
            authStore: useAuthStore(),
            model: { labels: [], cwes: [] },
            previewData: null,
            showPreview: false,
            templateChoices: [],
            loading: false,
            loaded: false,
            downloadPending: false
        };
    },
    computed: {
        previewUrl() {
            let blob = new Blob([this.previewData], { type: 'application/pdf' });
            return URL.createObjectURL(blob);
        },
        containerCol() {
            return this.showPreview ? 'col-span-6' : 'col-span-12';
        }
    },
    methods: {
        update() {
            this.loading = true;
            const data = {
                title: this.model.title,
                technology: this.model.technology?.pk,
                affected_versions: this.model.affected_versions,
                fixed_version: this.model.fixed_version,
                hide_advisory_id_in_report: this.model.hide_advisory_id_in_report,
                custom_report_title: this.model.custom_report_title,
                cve_id: this.model.cve_id,
                researchers: this.model.researchers,
                report_template: this.model.report_template?.name,
                cvss_vector: this.model.cvss_vector,
                description: this.model.description,
                proof_text: this.model.proof_text,
                recommendation: this.model.recommendation,
                labels: this.model.labels.map((item) => item.pk || item),
                cwes: this.model.cwes.map((item) => item.pk || item)
            };

            this.$api
                .patch(this.$api.e.advisoryDetail, { pk: this.advisoryId }, data)
                .then((response) => {
                    this.$toaster({
                        title: 'Advisory updated!',
                        duration: 3000,
                        description: 'Advisory was updated successfully!'
                    });
                    this.getPreviewData();
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getAdvisory() {
            this.$api.get(this.$api.e.advisoryDetail, { pk: this.advisoryId }).then((response) => {
                this.model = response.data;
                this.templateChoices.push(response.data.vulnerability);
                this.loaded = true;
            });
        },
        getPreviewData() {
            const config = { responseType: 'arraybuffer' };
            this.$api.get(this.$api.e.aPreview, { pk: this.advisoryId }, null, config).then((response) => {
                this.previewData = response.data;
            });
        },
        togglePreview() {
            this.showPreview = !this.showPreview;
            if (this.showPreview) this.getPreviewData();
            else this.previewData = null;
        },
        downloadAsPDF() {
            this.downloadPending = true;
            const params = {};
            if (this.model.report_template) params.template = this.model.report_template.name;

            this.$api
                .get(this.$api.e.aDownloadPdf, { aPk: this.advisoryId }, params, { responseType: 'arraybuffer' })
                .then(this.forceFileDownload)
                .finally(() => {
                    this.downloadPending = false;
                });
        },
        forceFileDownload(response) {
            const blob = new Blob([response.data], { type: response.headers['Content-Type'] });
            const filename = response.headers['content-disposition'].split('filename=')[1].split(';')[0];
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            link.click();
        },
        onImageUpload(file, onSuccess) {
            const data = new FormData();
            data.append('image', file);
            this.$api.post(this.$api.e.aAttachmentList, { aPk: this.advisoryId }, data).then((resp) => onSuccess(resp.data.storage_link));
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this advisory?',
                header: 'Delete confirmation',
                accept: () => {
                    this.$api.delete(this.$api.e.advisoryDetail, { pk: this.advisoryId }).then(() => {
                        this.$toaster({
                            title: 'Confirmed',
                            description: 'Advisory deleted!',
                            duration: 3000
                        });
                        this.$router.push({
                            name: 'AdvisoryList'
                        });
                    });
                }
            });
        }
    },
    mounted() {
        this.getAdvisory();
    },
    components: {
        BackLinkButton,
        PageHeader,
        ContainerLayout,
        DefaultSkeleton,
        MultiModelCombobox,
        ModelCombobox,
        Card,
        Switch,
        Input,
        Button,
        ReloadIcon,
        MarkdownEditor,
        Field,
        InlineField,
        InlineFieldGroup
    }
};
</script>

<template>
    <ContainerLayout>
        <BackLinkButton text="Back to Advisory" :href="$router.resolve({ name: 'AdvisoryDetail', params: { advisoryId } }).href" />
        <PageHeader>Update Advisory</PageHeader>

        <div class="flex justify-end gap-2 mb-4">
            <Button variant="outline" @click="togglePreview"> <i class="fa fa-eye"></i> Preview </Button>
            <Button :disabled="downloadPending" variant="default" @click="downloadAsPDF">
                <ReloadIcon v-if="downloadPending" class="w-4 h-4 mr-2 animate-spin" />
                <i class="fa fa-download"></i> Download
            </Button>
            <Button variant="destructive" @click="confirmDialogDelete"><i class="fa fa-trash"></i> Delete</Button>
        </div>

        <div class="grid grid-cols-12 gap-4">
            <div :class="containerCol">
                <Form v-if="loaded">
                    <InlineFieldGroup>
                        <InlineField label="CWEs">
                            <MultiModelCombobox v-model="model.cwes" title="" :options-url="$api.e.cweList" label-field="name" value-field="pk" variant="form" />
                        </InlineField>
                        <InlineField label="Title">
                            <Input id="title" v-model="model.title" />
                        </InlineField>
                    </InlineFieldGroup>

                    <Field label="Product">
                        <ModelCombobox v-model="model.technology" :api-endpoint="$api.e.technologyList" label-field="name" value-field="pk" variant="form" />
                    </Field>

                    <InlineFieldGroup>
                        <InlineField label="Affected Versions">
                            <Input id="affected_versions" v-model="model.affected_versions" />
                        </InlineField>
                        <InlineField label="Fixed Version">
                            <Input id="fixed_version" v-model="model.fixed_version" />
                        </InlineField>
                    </InlineFieldGroup>

                    <Field label="CVSS">
                        <Input id="cvss_vector" v-model="model.cvss_vector" />
                    </Field>

                    <Field label="Labels">
                        <MultiModelCombobox v-model="model.labels" :options-url="$api.e.aLabelList" label-field="name" value-field="pk" />
                    </Field>

                    <InlineFieldGroup>
                        <InlineField label="Report Template">
                            <ModelCombobox v-model="model.report_template" :api-endpoint="$api.e.reportTemplateList" label-field="name" value-field="name" variant="form" />
                        </InlineField>
                        <InlineField label="Custom Report Title">
                            <Input id="custom_title" v-model="model.custom_report_title" />
                        </InlineField>
                    </InlineFieldGroup>

                    <InlineFieldGroup>
                        <InlineField label="Researchers">
                            <Input id="researchers" v-model="model.researchers" />
                            <small class="text-xs">Overwrites the researchers section in the report.</small>
                        </InlineField>
                        <InlineField label="CVE-ID">
                            <Input id="cve_id" v-model="model.cve_id" />
                        </InlineField>
                    </InlineFieldGroup>

                    <Field>
                        <div class="flex items-center">
                            <Switch v-model:checked="model.hide_advisory_id_in_report" />
                            <label class="ml-3">Hide advisory ID in report?</label>
                        </div>
                    </Field>

                    <Field label="Description">
                        <MarkdownEditor v-model="model.description" />
                    </Field>

                    <Field label="Proof">
                        <MarkdownEditor v-model="model.proof_text" :show-upload-button="true" @upload="onImageUpload" />
                    </Field>

                    <Field label="Recommendation">
                        <MarkdownEditor v-model="model.recommendation" />
                    </Field>

                    <Button class="w-full mt-4" @click="update">
                        <ReloadIcon v-if="loading" class="w-4 h-4 mr-2 animate-spin" />
                        Save
                    </Button>
                </Form>

                <Card v-else>
                    <DefaultSkeleton />
                </Card>
            </div>

            <div v-if="showPreview" class="col-span-6 border rounded-lg">
                <DefaultSkeleton v-if="!previewData" />
                <iframe v-if="previewData" :src="previewUrl" class="w-full h-full min-h-[75vh] rounded" />
            </div>
        </div>
    </ContainerLayout>
</template>
