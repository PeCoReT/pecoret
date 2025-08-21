<script>
import { FindingTabMenu } from '@/partials/projects';
import { CVSS31CalculatorForm, CVSS4CalculatorForm } from '@/partials/common';
import { useAuthStore } from '@/store/auth';
import { BlankSlate } from '@/components/blankslate';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'ScoreList',
    components: { ContainerLayout, CVSS31CalculatorForm, BlankSlate, CVSS4CalculatorForm, FindingTabMenu },
    mounted() {
        this.getFinding();
    },
    methods: {
        getFinding() {
            this.$api.get(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.findingId }).then((response) => {
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
            breadcrumbs: [
                {
                    label: 'Findings',
                    route: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.$route.params.projectId }
                    }).path
                },
                {
                    label: 'Finding Detail',
                    route: this.$router.resolve({
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
    <ContainerLayout>
        <template #left-header>
            <FindingTabMenu class="mb-3"></FindingTabMenu>
            <div v-if="authStore.activeProject.require_cvss_score === 0" class="col-span-12 gap-3">
                <div class="grid grid-cols-2 mb-2">
                    <div class="col-span-1">
                        <p class="text-xl">CVSS 4.0 Base-Score</p>
                    </div>
                    <div class="col-span-1">
                        <div class="justify-end flex">
                            <span :class="'color-severity severity-' + this.cvss4.severity.toLowerCase()">{{ this.cvss4.vector }} / {{ this.cvss4.score }} ({{ this.cvss4.severity }})</span>
                        </div>
                    </div>
                </div>

                <CVSS4CalculatorForm v-model="cvss4" @update:score="this.onScoreUpdate"></CVSS4CalculatorForm>
            </div>
            <div v-else-if="authStore.activeProject.require_cvss_score === 1" class="col-span-12 gap-3">
                <div class="grid grid-cols-2 mb-2">
                    <div class="col-span-1">
                        <p class="text-xl">CVSS 3.1 Base-Score</p>
                    </div>
                    <div class="col-span-1">
                        <div class="justify-end flex">
                            <span :class="'color-severity severity-' + this.cvss31.severity.toLowerCase()">{{ this.cvss31.vector }} / {{ this.cvss31.score }} ({{ this.cvss31.severity }})</span>
                        </div>
                    </div>
                </div>
                <CVSS31CalculatorForm v-model="cvss31" class="mt-3" @update:score="this.onCVSS31Update"></CVSS31CalculatorForm>
            </div>

            <div v-else class="card col-span-12">
                <BlankSlate icon="fa fa-calculator" text="No scores are configured for this project" title="Scores disabled"></BlankSlate>
            </div>
        </template>
    </ContainerLayout>
</template>
