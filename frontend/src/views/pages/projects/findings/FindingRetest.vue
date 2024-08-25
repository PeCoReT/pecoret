<script>
import FindingService, { statusChoices } from '@/service/FindingService';
import FindingTabMenu from '@/components/navigation/FindingTabMenu.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'FindingRetest.vue',
    components: { FindingTabMenu, MarkdownEditor },
    props: {
        findingId: {
            required: true
        },
        projectId: {
            required: true
        }
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            this.service.getFinding(this.projectId, this.findingId).then((response) => {
                this.finding = response.data;
                this.model.status = response.data.status;
                this.model.retest_results = response.data.retest_results;
                this.model.date_retested = response.data.date_retested;
            });
        },
        patchFinding() {
            this.loading = true;
            this.service
                .patchFinding(this.$api, this.projectId, this.findingId, this.model)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Finding updated!',
                        life: 3000,
                        detail: 'Finding was updated successfully!'
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    data() {
        return {
            service: new FindingService(),
            loading: false,
            finding: { component: {} },
            model: {
                retest_results: null,
                date_retested: null,
                status: null
            },
            statusChoices: statusChoices,
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.projectId }
                    })
                },
                {
                    label: 'Finding Detail',
                    to: this.$router.resolve({
                        name: 'FindingDetail',
                        params: { projectId: this.projectId, findingId: this.findingId }
                    })
                },
                {
                    label: 'Retest',
                    disabled: true
                }
            ]
        };
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid grid-cols-2 mt-3">
        <div class="col-span-1">
            <div class="justify-start flex">
                <strong class="text-lg" v-if="finding.vulnerability">{{ finding.vulnerability.name }} / {{ finding.name }}</strong>
            </div>
        </div>
        <div class="col-span-1">
            <div class="flex justify-end"></div>
        </div>
    </div>
    <div class="grid grid-cols-1 mt-3">
        <div class="col-span-1">
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <div class="card border-noround-top">
                <Form>
                    <Field label="Status">
                        <Select v-model="model.status" :options="statusChoices" optionValue="value" optionLabel="title" class="w-full"></Select>
                    </Field>
                    <Field label="Date Retested">
                        <DatePicker v-model="model.date_retested" id="date_retested"></DatePicker>
                    </Field>
                    <Field label="Retest Summary">
                        <MarkdownEditor v-model="model.retest_results" id="retest"></MarkdownEditor>
                    </Field>
                    <Button class="w-full" label="Save" :loading="loading" @click="patchFinding"></Button>
                </Form>
            </div>
        </div>
    </div>
</template>
