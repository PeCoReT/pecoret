<script>
import ReportTabMenu from '@/components/pages/ReportTabMenu.vue';
import ReportService from '@/service/ReportService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ExecutiveSummary',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Reports',
                    to: this.$router.resolve({
                        name: 'ReportList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Report Detail',
                    to: this.$router.resolve({
                        name: 'ReportDetail',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Executive Summary',
                    disabled: true
                }
            ],
            model: {
                evaluation: '',
                recommendation: ''
            },
            reportService: new ReportService(),
            reportId: this.$route.params.reportId,
            projectId: this.$route.params.projectId,
            saveLoading: false
        };
    },
    mounted() {
        this.getItem();
    },
    methods: {
        getItem() {
            this.reportService.getReport(this.$api, this.projectId, this.reportId).then((response) => {
                this.model = response.data;
            });
        },
        updateReport() {
            this.saveLoading = true;
            let data = {
                recommendation: this.model.recommendation,
                evaluation: this.model.evaluation
            };
            this.reportService
                .updateReport(this.$api, this.projectId, this.reportId, data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Report updated!',
                        life: 3000,
                        detail: 'Report was updated successfully!'
                    });
                })
                .finally(() => {
                    this.saveLoading = false;
                });
        }
    },
    components: { ReportTabMenu, MarkdownEditor }
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
            <ReportTabMenu class="surface-card"></ReportTabMenu>
            <div class="card border-noround-top">
                <div class="grid formgrid p-fluid">
                    <div class="field col-12">
                        <label for="evaluation">Evaluation</label>
                        <MarkdownEditor v-model="model.evaluation"></MarkdownEditor>
                    </div>
                    <div class="field col-12">
                        <label for="recommendation">Recommendation</label>
                        <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
                    </div>
                    <div class="field col-12">
                        <Button @click="updateReport" label="Save" :loading="saveLoading === true"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>