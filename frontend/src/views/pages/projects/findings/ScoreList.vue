<script>
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';
import CVSS4CalculatorForm from '@/components/forms/CVSS4CalculatorForm.vue';
import { useAuthStore } from '@/store/auth';
import BlankSlate from '@/components/BlankSlate.vue';
import CVSS31CalculatorForm from '@/components/forms/CVSS31CalculatorForm.vue';

export default {
    name: 'ScoreList',
    components: { CVSS31CalculatorForm, BlankSlate, CVSS4CalculatorForm, FindingTabMenu },
    mounted() {
        this.getFinding();
    },
    methods: {
        getFinding() {
            this.service.getFinding(this.projectId, this.findingId).then((response) => {
                this.cvss4.vector = response.data.cvss_score_40;
                this.cvss31.vector = response.data.cvss_score_31;
            });
        },
        onScoreUpdate(obj) {
            this.cvss4.score = obj.score;
            this.cvss4.severity = obj.severity;
        },
        onCVSS31Update(obj) {
            this.cvss31.score = obj.score;
            this.cvss31.severity = obj.severity;
        }
    },
    data() {
        return {
            authStore: useAuthStore(),
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            service: new FindingService(),
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.$route.params.projectId }
                    }).path
                },
                {
                    label: 'Finding Detail',
                    to: this.$router.resolve({
                        name: 'FindingDetail',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: 'Scores',
                    disabled: true
                }
            ],
            cvss4: { severity: 'Informational', score: 0.0, vector: '' },
            cvss31: { severity: 'Informational', score: 0.0, vector: '' }
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
        <div class="col-12">
            <FindingTabMenu class="surface-card"></FindingTabMenu>

            <div class="card border-noround-top" v-if="authStore.activeProject.require_cvss_score === 0">
                <div class="grid">
                    <div class="col-6">
                        <p class="text-xl">CVSS 4.0 Base-Score</p>
                    </div>
                    <div class="col-6">
                        <div class="justify-content-end flex">
                            <span :class="'color-severity severity-' + this.cvss4.severity.toLowerCase()">{{ this.cvss4.vector }} / {{ this.cvss4.score }} ({{ this.cvss4.severity }})</span>
                        </div>
                    </div>
                </div>

                <CVSS4CalculatorForm v-model="cvss4" @update:score="this.onScoreUpdate"></CVSS4CalculatorForm>
            </div>

            <div class="card border-noround-top" v-else-if="authStore.activeProject.require_cvss_score === 1">
                <div class="grid">
                    <div class="col-6">
                        <p class="text-xl">CVSS 3.1 Base-Score</p>
                    </div>
                    <div class="col-6">
                        <div class="justify-content-end flex">
                            <span :class="'color-severity severity-' + this.cvss31.severity.toLowerCase()">{{ this.cvss31.vector }} / {{ this.cvss31.score }} ({{ this.cvss31.severity }})</span>
                        </div>
                    </div>
                </div>
                <CVSS31CalculatorForm v-model="cvss31" @update:score="this.onCVSS31Update"></CVSS31CalculatorForm>
            </div>

            <div class="card border-noround-top" v-else>
                <BlankSlate title="Scores disabled" text="No scores are configured for this project" icon="fa fa-calculator"></BlankSlate>
            </div>
        </div>
    </div>
</template>