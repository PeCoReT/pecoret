<script>
import FindingService, { statusChoices } from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';
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
    <div class="grid">
        <div class="col-6">
            <div class="justify-content-start flex"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end"></div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <div class="card border-noround-top">
                <div class="grid formgrid p-fluid">
                    <div class="col-12 field md:col-6">
                        <label for="status">Status</label>
                        <Dropdown v-model="model.status" :options="statusChoices" optionValue="value" optionLabel="title" class="w-full"></Dropdown>
                    </div>
                    <div class="col-12 field md:col-6">
                        <label for="date_retested">Date Retested</label>
                        <Calendar v-model="model.date_retested" id="date_retested"></Calendar>
                    </div>
                    <div class="col-12 field">
                        <label for="retest">Retest Summary</label>
                        <MarkdownEditor v-model="model.retest_results" id="retest"></MarkdownEditor>
                    </div>
                    <div class="col-12">
                        <Button label="Save" :loading="loading" @click="patchFinding"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
