<script>
import { AdvisoryTabMenu } from '@/partials/advisories';
import { useAuthStore } from '@/store/auth';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { Card, DetailCardWithIcon, InfoCardWithForm } from '@/components/card';
import { Button } from '@/components/ui/button';
import { ReloadIcon } from '@radix-icons/vue';
import { PageHeader } from '@/components/typography';
import { DatePicker } from '@/components/datepicker';
import { Select } from '@/components/select';
import { advisoryStatusChoices, severityChoices, vulnerabilityStatusChoices } from '@/utils/constants';

export default {
    name: 'AdvisoryDetail',
    mounted() {
        this.getAdvisory();
    },
    data() {
        return {
            advisoryId: this.$route.params.advisoryId,
            authStore: useAuthStore(),
            advisory: { vulnerability: {}, technology: {}, user: {} },
            loading: false,
            statusChoices: advisoryStatusChoices,
            vulnerabilityStatusChoices: vulnerabilityStatusChoices,
            exportTemplate: null,
            severityChoices: severityChoices,
            downloadPending: false
        };
    },
    methods: {
        getAdvisory() {
            this.loading = true;
            this.$api
                .get(this.$api.e.advisoryDetail, { pk: this.advisoryId })
                .then((response) => {
                    this.advisory = response.data;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        patchAdvisory(data) {
            this.$api.patch(this.$api.e.advisoryDetail, { pk: this.advisoryId }, data).then((response) => {
                this.advisory = response.data;
                if (this.showPreview === true) {
                    this.getPreviewData();
                }
                this.$toaster({
                    title: 'Advisory updated!',
                    duration: 3000,
                    description: 'Advisory was updated!'
                });
            });
        },
        patchAdvisoryDisclosureDate() {
            let data = {
                date_planned_disclosure: this.advisory.date_planned_disclosure.toISOString().split('T')[0]
            };
            this.patchAdvisory(data);
        },
        forceFileDownload(response) {
            let blob = new Blob([response.data], { type: response.headers['Content-Type'] });
            let filename = response.headers['content-disposition'].split('filename=')[1].split(';')[0];
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            link.click();
            this.downloadPending = false;
        },
        downloadAsPDF() {
            this.downloadPending = true;
            let params = {};
            if (this.exportTemplate) {
                params['template'] = this.exportTemplate;
            }
            this.$api
                .get(this.$api.e.aDownloadPdf, { aPk: this.advisoryId }, params, { responseType: 'arraybuffer' })
                .then((response) => {
                    this.forceFileDownload(response);
                    this.exportTemplate = null;
                })
                .finally(() => {
                    this.downloadPending = false;
                });
        }
    },
    computed: {
        productDisplay() {
            if (this.advisory.technology && this.advisory.technology.vendor) {
                return `${this.advisory.technology.name} (by ${this.advisory.technology.vendor})`;
            }
            return `${this.advisory.technology.name} (by Unknown)`;
        }
    },
    components: {
        DefaultSkeleton,
        Card,
        Select,
        DatePicker,
        ContainerLayout,
        DetailCardWithIcon,
        AdvisoryTabMenu,
        InfoCardWithForm,
        Button,
        ReloadIcon,
        PageHeader
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <div class="flex justify-start">
                <AdvisoryTabMenu></AdvisoryTabMenu>
            </div>
        </template>
        <template #right-header>
            <div class="flex justify-end gap-1">
                <Button :disabled="downloadPending" variant="default" @click="downloadAsPDF">
                    <ReloadIcon v-if="downloadPending" class="w-4 h-4 mr-2 animate-spin"></ReloadIcon>
                    <i class="fa fa-download"></i> Download
                </Button>
                <Button variant="outline" @click="this.$router.push({ name: 'AdvisoryUpdate', params: { advisoryId: this.advisoryId } })"> <i class="fa fa-pen-to-square"></i> Edit </Button>
            </div>
        </template>

        <PageHeader>Advisory: {{ advisory.title }}</PageHeader>

        <div class="col-span-12">
            <div v-if="loading === false">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon :text="productDisplay" class="bg-background" icon="fa fa-cart-shopping" title="Product"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon :text="advisory.affected_versions" class="bg-background" icon="fa fa-circle-exclamation" title="Affected Versions"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon :text="advisory.fixed_version || '-'" class="bg-background" icon="fa fa-screwdriver-wrench" title="Fixed Versions"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon :text="advisory.user.username" class="bg-background" icon="fa fa-user" title="User"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid grid-cols-12 mt-3 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-background w-full" icon="fa fa-shield-halved" title="Severity">
                            <Select v-model="advisory.severity" :options="severityChoices" @update:modelValue="patchAdvisory({ severity: advisory.severity })"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-background w-full" icon="fa fa-file-pen" title="Vulnerability Status">
                            <Select v-model="advisory.vulnerability_status" :options="vulnerabilityStatusChoices" @update:modelValue="patchAdvisory({ vulnerability_status: advisory.vulnerability_status })"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-background w-full" icon="fa fa-bookmark" title="Status">
                            <Select v-model="advisory.status" :options="statusChoices" @update:modelValue="patchAdvisory({ status: advisory.status })"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-background w-ull" icon="fa-calendar" title="Planned Disclosure">
                            <DatePicker v-model="advisory.date_planned_disclosure" @update:modelValue="patchAdvisoryDisclosureDate"></DatePicker>
                        </InfoCardWithForm>
                    </div>
                </div>
                <div class="grid grid-cols-12 mt-3">
                    <div class="col-span-12 space-y-4">
                        <h2 class="text-xl font-semibold">Description</h2>
                        <div class="markdown-block"><div v-html="advisory.description_html"></div></div>

                        <h2 class="text-xl font-semibold">Proof</h2>
                        <div class="markdown-block"><div v-html="advisory.proof_html || '-'"></div></div>

                        <h2 class="text-xl font-semibold">Recommendation</h2>
                        <div class="markdown-block"><div v-html="advisory.recommendation_html || '-'"></div></div>
                    </div>
                </div>
            </div>

            <Card v-else>
                <DefaultSkeleton></DefaultSkeleton>
            </Card>
        </div>
    </ContainerLayout>
</template>
