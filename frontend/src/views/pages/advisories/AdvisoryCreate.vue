<script>
import AdvisoryService from '@/service/AdvisoryService';
import VulnerabilityTemplateService from '@/service/VulnerabilityTemplateService';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'AdvisoryCreate',
    data() {
        return {
            service: new AdvisoryService(),
            templateService: new VulnerabilityTemplateService(),
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            activeStep: 0,
            stepItems: [
                {
                    label: 'Vendor & Description'
                },
                {
                    label: 'Proof of Concept'
                },
                {
                    label: 'Recommendation'
                }
            ],
            model: {
                internal_name: null,
                template: null,
                product: null,
                affected_versions: null,
                fixed_version: null,
                severity: null,
                vendor_name: null,
                vendor_url: null,
                attachments: []
            },
            loading: false,
            templateChoices: []
        };
    },
    methods: {
        async create() {
            let proof_text = this.model.proof_text;
            this.loading = true;
            let data = {
                internal_name: this.model.internal_name,
                vulnerability_id: this.model.template,
                product: this.model.product,
                description: this.model.description,
                affected_versions: this.model.affected_versions,
                fixed_version: this.model.fixed_version,
                severity: this.model.severity,
                vendor_name: this.model.vendor_name,
                vendor_url: this.model.vendor_url
            };
            // create advisory first, so we can upload attachments afterward
            let response = await this.service.createAdvisory(this.$api, data);
            let response2 = null;
            for (let i = 0; i < this.model.attachments.length; i++) {
                let attachment = this.model.attachments[i];
                let data = new FormData();
                data.append('image', attachment);
                response2 = await this.service.attachmentCreate(this.$api, response.data.pk, data);
                // replace attachment link in proof_text
                proof_text = proof_text.replace(`(${attachment.objectURL})`, `(${response2.data.image})`);
            }
            await this.service.patchAdvisory(this.$api, response.data.pk, { proof_text: proof_text });
            this.$router.push({
                name: 'AdvisoryDetail',
                params: {
                    advisoryId: response.data.pk
                }
            });
            this.loading = false;
        },
        onAttachmentSelected(event) {
            this.model.attachments.push(event.files[event.files.length - 1]);
        },
        preSelectTemplateValues() {
            this.templateChoices.forEach((item) => {
                if (item.vulnerability_id === this.model.template) {
                    this.model.severity = item.severity;
                    this.model.recommendation = item.recommendation;
                }
            });
        },
        onFocusTemplate() {
            this.templateService.getTemplates(this.$api).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        onFilterTemplate(event) {
            let params = {
                search: event.value
            };
            this.templateService.getTemplates(this.$api, params).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        copyLinkToClipboard(attachment) {
            let md_data = `![${attachment.name}](${attachment.objectURL})`;
            navigator.clipboard.writeText(md_data);
            this.$toast.add({
                severity: 'info',
                summary: 'Copied to clipboard',
                detail: 'Link copied to clipboard',
                life: 2000
            });
        },
        deleteAttachment(attachment) {
            this.model.attachments = this.model.attachments.filter((item) => item.objectURL !== attachment.objectURL);
        }
    },
    mounted() {},
    components: { SeveritySelectField, MarkdownEditor }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <Steps v-model:activeStep="activeStep" :model="stepItems" class="mb-3"></Steps>

                <div class="p-fluid formgrid grid" v-if="activeStep === 0">
                    <div class="field col-12">
                        <label for="name">Internal Name</label>
                        <InputText id="name" v-model="model.internal_name"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="template">Vulnerability Template</label>
                        <Dropdown :options="templateChoices" optionLabel="name" optionValue="vulnerability_id" @change="preSelectTemplateValues" @focus="onFocusTemplate" filter @filter="onFilterTemplate" v-model="model.template"></Dropdown>
                    </div>
                    <div class="field col-12 md:col-6">
                        <SeveritySelectField v-model="model.severity"></SeveritySelectField>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="product">Product</label>
                        <InputText id="product" v-model="model.product"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="affected_versions">Affected Versions</label>
                        <InputText id="affected_versions" v-model="model.affected_versions"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_name">Vendor</label>
                        <InputText id="vendor_name" v-model="model.vendor_name"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_url">Vendor URL</label>
                        <InputText id="vendor_url" v-model="model.vendor_url"></InputText>
                    </div>
                    <div class="field col-12">
                        <label for="description">Description</label>
                        <MarkdownEditor v-model="model.description"></MarkdownEditor>
                    </div>
                    <div class="mt-3 col-12">
                        <div class="justify-content-end flex">
                            <Button label="Next" @click="activeStep = 1"></Button>
                        </div>
                    </div>
                </div>
                <div class="p-fluid formgrid grid" v-else-if="activeStep === 1">
                    <div class="field col-12">
                        <label for="proof">Proof</label>
                        <MarkdownEditor id="proof" v-model="model.proof_text"></MarkdownEditor>
                    </div>
                    <div class="field col-12">
                        <FileUpload name="attachments[]" :multiple="true" accept="image/*" :maxFileSize="1000000" @select="onAttachmentSelected">
                            <template #header="{ chooseCallback }">
                                <div class="row">
                                    <div class="col">
                                        <Button @click="chooseCallback()" icon="fa fa-upload pl-4 pr-4" outlined></Button>
                                    </div>
                                </div>
                            </template>
                            <template #content>
                                <div v-if="model.attachments.length > 0">
                                    <div class="flex flex-wrap gap-5">
                                        <div v-for="file in model.attachments" :key="file.name" class="card flex flex-column border-1 surface-border align-items-center gap-4">
                                            <div @click="copyLinkToClipboard(file)">
                                                <img role="presentation" :alt="file.name" :src="file.objectURL" width="100" height="50" class="shadow-2" />
                                            </div>
                                            <span class="font-semibold">{{ file.name }}</span>
                                            <Button @click="deleteAttachment(file)" label="Delete Attachment" class="p-0 m-0" link severity="danger"></Button>
                                        </div>
                                    </div>
                                </div>
                                <div v-else class="flex align-items-center justify-content-center flex-column">
                                    <i class="pi pi-cloud-upload border-2 border-circle p-5 text-8xl text-400 border-400" />
                                    <p class="mt-4 mb-0">Drag and drop files here to upload.</p>
                                </div>
                            </template>
                        </FileUpload>
                    </div>
                    <div class="mt-3 col-12">
                        <div class="grid">
                            <div class="justify-content-end col-6 flex">
                                <Button label="Back" @click="activeStep = 0" outlined></Button>
                            </div>
                            <div class="justify-content-end col-6 flex">
                                <Button label="Next" @click="activeStep = 2"></Button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-fluid formgrid grid" v-else-if="activeStep === 2">
                    <div class="field col-12">
                        <label for="recommendation">Recommendation</label>
                        <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
                    </div>
                    <div class="mt-3 col-12">
                        <div class="grid">
                            <div class="justify-content-end col-6 flex">
                                <Button label="Back" @click="activeStep = 1" outlined :disabled="loading"></Button>
                            </div>
                            <div class="justify-content-end col-6 flex">
                                <Button label="Save" :loading="loading" @click="create"></Button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
