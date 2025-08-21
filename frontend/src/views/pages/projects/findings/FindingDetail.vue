<script>
import { FindingAsAdvisoryDialog, FindingTabMenu } from '@/partials/projects';
import { FileDrop } from '@/components/form';
import { MarkdownEditor } from '@/components/editor';
import { findingStatusChoices, severityChoices } from '@/utils/constants';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import forceFileDownload from '@/utils/file';
import { DetailCardWithIcon, InfoCardWithForm } from '@/components/card';
import { Switch } from '@/components/ui/switch';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { Select } from '@/components/select';
import { DatePicker } from '@/components/datepicker';
import {DateFormatter, getLocalTimeZone} from "@internationalized/date";

export default {
    name: 'FindingDetail',
    mounted() {
        this.getFinding();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            finding: { asset: {} },
            showPreview: false,
            previewData: null,
            previewLoading: false,
            userAccountChoices: [],
            showAsAdvisoryModal: false,
            downloadPending: false
        };
    },
    computed: {
        containerCol() {
            if (this.showPreview === true) {
                return 'col-span-6';
            }
            return 'col-span-12';
        },
        previewUrl() {
            let blob = new Blob([this.previewData], { type: 'application/pdf' });
            return URL.createObjectURL(blob);
        },
        userAccountDisplay() {
            if (this.finding.user_account && this.finding.user_account.username !== '') {
                return this.finding.user_account.username;
            }
            return '-';
        }
    },
    methods: {
        findingStatusChoices() {
            return findingStatusChoices;
        },
        severityChoices() {
            return severityChoices;
        },
        getFinding() {
            this.$api.get(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.findingId }).then((response) => {
                this.finding = response.data;
            });
        },
        onUserAccountFocus() {
            if (this.userAccountChoices.length) {
                return;
            }
            this.$api.get(this.$api.e.pAccountList, { projectPk: this.projectId }).then((response) => {
                this.userAccountChoices = response.data.results;
            });
        },
        deleteFinding() {
            this.$api.delete(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.findingId }).then(() => {
                this.$toaster({ title: 'Confirmed', description: 'Finding deleted!', duration: 3000 });
                this.$router.push({ name: 'FindingList', params: { projectId: this.projectId } });
            });
        },
        patchFindingData(data) {
            this.$api
                .patch(
                    this.$api.e.pFindingDetail,
                    {
                        pPk: this.projectId,
                        pk: this.finding.pk
                    },
                    data
                )
                .then((response) => {
                    this.finding = response.data;
                    if (this.showPreview === true) {
                        this.getPreviewData();
                    }
                    this.$toaster({ title: 'Updated', description: 'Finding updated!', duration: 3000 });
                });
        },
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
        togglePreview() {
            this.showPreview = !this.showPreview;
            if (this.showPreview === true) {
                this.getPreviewData();
            } else {
                this.previewData = null;
            }
        },
        update() {
            let data = {
                exclude_from_report: this.finding.exclude_from_report,
                name: this.finding.name,
                recommendation: this.finding.recommendation,
                proof_text: this.finding.proof_text,
                entrypoint: this.finding.entrypoint
            };
            if (this.finding.user_account) {
                data['user_account'] = this.finding.user_account.pk;
            }
            this.patchFindingData(data);
        },
        getPreviewData() {
            this.previewLoading = true;
            let config = {
                responseType: 'arraybuffer'
            };
            this.$api
                .get(this.$api.e.pFindingPreview, { pPk: this.projectId, pk: this.findingId }, null, config)
                .then((response) => {
                    this.previewData = response.data;
                })
                .finally(() => {
                    this.previewLoading = false;
                });
        },
        downloadAsPDF() {
            this.$api
                .get(
                    this.$api.e.pFindingExportPdf,
                    {
                        pPk: this.projectId,
                        pk: this.findingId
                    },
                    null,
                    { responseType: 'arraybuffer' }
                )
                .then((response) => {
                    forceFileDownload(response);
                });
        },
        patchFindingDate(findingDate) {
            this.patchFindingData({finding_date: findingDate});
        }
    },
    components: {
        DefaultSkeleton,
        BaseLayout,
        MarkdownEditor,
        FindingTabMenu,
        DetailCardWithIcon,
        InfoCardWithForm,
        FindingAsAdvisoryDialog,
        FileDrop,
        Switch,
        Input,
        Checkbox,
        Select,
        Button,
        DatePicker
    }
};
</script>

<template>
    <BaseLayout>
        <template #pre-content-left>
            <div class="flex justify-start mt-8">
                <FindingTabMenu></FindingTabMenu>
            </div>
        </template>
        <template #pre-content-right>
            <div class="flex justify-end gap-2 mt-8">
                <FindingAsAdvisoryDialog v-model="showAsAdvisoryModal"></FindingAsAdvisoryDialog>
                <Button @click="togglePreview" variant="outline"> <i class="fa fa-eye" /> Preview </Button>
                <Button @click="downloadAsPDF" variant="outline"> <i class="fa fa-download" /> Download </Button>
                <Button
                    variant="outline"
                    @click="
                        () => {
                            showAsAdvisoryModal = true;
                        }
                    "
                >
                    <i class="fa fa-copy"></i> Advisory
                </Button>
                <Button variant="destructive" @click="confirmDialogDelete"> <i class="fa fa-trash"></i> Delete </Button>
            </div>
        </template>
        <div :class="containerCol">
            <div class="grid grid-cols-12 gap-3">
                <div class="col-span-12 md:col-span-4">
                    <DetailCardWithIcon :text="finding.asset.name" class="bg-surface-950" icon="fa-crosshairs" title="Asset"></DetailCardWithIcon>
                </div>
                <div class="col-span-12 md:col-span-4">
                    <DetailCardWithIcon :text="userAccountDisplay" class="bg-surface-950" icon="fa-user" title="User Account"></DetailCardWithIcon>
                </div>
                <div class="col-span-12 md:col-span-4">
                    <DetailCardWithIcon :text="finding.status" class="bg-surface-950" icon="fa-bookmark" title="Status"></DetailCardWithIcon>
                </div>
            </div>
            <div class="grid mt-3 grid-cols-12 gap-3">
                <div class="col-span-12 md:col-span-3">
                    <InfoCardWithForm class="bg-surface-950 w-full" icon="fa-bookmark" title="Status">
                        <Select v-model="finding.status" :options="findingStatusChoices()" class="w-full" @change="patchFindingData({ status: finding.status })"></Select>
                    </InfoCardWithForm>
                </div>
                <div class="col-span-12 md:col-span-3">
                    <InfoCardWithForm class="bg-surface-950" icon="fa-calendar" title="Finding Date">
                        <DatePicker v-model="finding.finding_date" dateFormat="yy-mm-dd" @update:modelValue="patchFindingDate"></DatePicker>
                    </InfoCardWithForm>
                </div>
                <div class="col-span-12 md:col-span-3">
                    <InfoCardWithForm class="bg-surface-950" icon="fa fa-shield-halved" title="Severity">
                        <Select v-model="finding.severity" :options="severityChoices()" optionLabel="label" optionValue="value" @change="patchFindingData({ severity: finding.severity })"></Select>
                    </InfoCardWithForm>
                </div>
                <div class="col-span-12 md:col-span-3">
                    <InfoCardWithForm class="bg-surface-950" icon="fa-user-tag" title="Needs review?">
                        <Switch v-model:checked="finding.needs_review" @update:checked="patchFindingData({ needs_review: finding.needs_review })"></Switch>
                    </InfoCardWithForm>
                </div>
            </div>

            <div class="grid grid-cols-12 gap-4 mt-3">
                <div class="col-span-12">
                    <Form>
                        <Field label="Name">
                            <Input v-model="finding.name"></Input>
                        </Field>
                        <Field label="Account">
                            <Select v-model="finding.user_account" :options="userAccountChoices" optionLabel="username" show-clear @focus="onUserAccountFocus"></Select>
                        </Field>
                        <Field label="Entrypoint">
                            <Input v-model="finding.entrypoint" type="text"></Input>
                        </Field>
                        <Field label="Proof">
                            <MarkdownEditor v-model="finding.proof_text"></MarkdownEditor>
                        </Field>
                        <Field>
                            <FileDrop></FileDrop>
                        </Field>
                        <Field label="Custom Recommendation">
                            <MarkdownEditor v-model="finding.recommendation"></MarkdownEditor>
                        </Field>
                        <Field>
                            <div class="flex align-items-center">
                                <Checkbox v-model:checked="finding.exclude_from_report" />
                                <label class="ml-2"> Exclude from report? </label>
                            </div>
                        </Field>
                        <Button class="w-full" @click="update">Save</Button>
                    </Form>
                </div>
            </div>
        </div>

        <div :class="containerCol" class="border rounded-lg">
            <DefaultSkeleton v-if="!this.previewData && this.showPreview === true" class="h-1rem"></DefaultSkeleton>
            <iframe v-if="previewLoading !== true && this.previewData" :key="previewData" :src="this.previewUrl" class="w-full h-full"></iframe>
        </div>
    </BaseLayout>
</template>
