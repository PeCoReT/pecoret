<script>
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';
import CVSS4CalculatorForm from '@/components/forms/CVSS4CalculatorForm.vue';

export default {
    name: 'ScoreList',
    components: { CVSS4CalculatorForm, FindingTabMenu },
    mounted() {
        this.getCVSS();
        this.getFinding();
    },
    methods: {
        getCVSS() {
            this.service.getCVSSScore(this.$api, this.projectId, this.findingId).then((response) => {
                this.model.base_cvss = response.data;
            });
        },
        patchCVSS(data) {
            this.service.patchCVSSScore(this.$api, this.projectId, this.findingId, this.model.base_cvss.pk, data).then((response) => {
                this.model.base_cvss = response.data;
            });
        },
        getFinding() {
            this.service.getFinding(this.projectId, this.findingId).then((response) => {
                this.cvss4.vector = response.data.cvss_score_40;
            });
        },
        onScoreUpdate(obj) {
            this.cvss4.score = obj.score;
            this.cvss4.severity = obj.severity;
        }
    },
    data() {
        return {
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
            model: {
                base_cvss: {
                    pk: null,
                    av: null,
                    ac: null,
                    pr: null,
                    ui: null,
                    s: null,
                    c: null,
                    i: null,
                    a: null
                }
            },
            cvss4: { severity: 'Informational', score: 0.0, vector: '' },
            cvssChoices: {
                av: [
                    { value: 'N', title: 'Network' },
                    { value: 'A', title: 'Adjacent Network' },
                    { value: 'L', title: 'Local' },
                    { value: 'P', title: 'Physical' }
                ],
                ac: [
                    { value: 'L', title: 'Low' },
                    { value: 'H', title: 'High' }
                ],
                pr: [
                    { value: 'N', title: 'None' },
                    { value: 'L', title: 'Low' },
                    { value: 'H', title: 'High' }
                ],
                ui: [
                    { value: 'N', title: 'None' },
                    { value: 'R', title: 'Required' }
                ],
                s: [
                    { value: 'U', title: 'Unchanged' },
                    { value: 'C', title: 'Changed' }
                ],
                cia: [
                    { value: 'N', title: 'None' },
                    { value: 'L', title: 'Low' },
                    { value: 'H', title: 'High' }
                ]
            }
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

            <div class="card border-noround-top">
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

            <div class="card">
                <p class="text-xl">CVSS Base-Score</p>

                <div class="grid">
                    <div class="col-6">
                        <div class="flex flex-column gap-2">
                            <label for="av">Attack Vector (AV)</label>
                            <Dropdown v-model="model.base_cvss.av" :options="cvssChoices.av" optionValue="value" @change="patchCVSS({ av: this.model.base_cvss.av })" optionLabel="title"></Dropdown>
                        </div>

                        <div class="flex flex-column gap-2">
                            <label for="av">Attack Complexity (AC)</label>
                            <Dropdown v-model="model.base_cvss.ac" :options="cvssChoices.ac" optionLabel="title" optionValue="value" @change="patchCVSS({ ac: this.model.base_cvss.ac })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="av">Privileges Required (PR)</label>
                            <Dropdown v-model="model.base_cvss.pr" :options="cvssChoices.pr" optionLabel="title" optionValue="value" @change="patchCVSS({ pr: this.model.base_cvss.pr })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="av">User Interaction (UI)</label>
                            <Dropdown v-model="model.base_cvss.ui" :options="cvssChoices.ui" optionLabel="title" optionValue="value" @change="patchCVSS({ ui: this.model.base_cvss.ui })"></Dropdown>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="flex flex-column gap-2">
                            <label for="av">Scope (S)</label>
                            <Dropdown v-model="model.base_cvss.s" :options="cvssChoices.s" optionLabel="title" optionValue="value" @change="patchCVSS({ s: this.model.base_cvss.s })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="av">Confidentiality (C)</label>
                            <Dropdown v-model="model.base_cvss.c" :options="cvssChoices.cia" optionLabel="title" optionValue="value" @change="patchCVSS({ c: this.model.base_cvss.c })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="av">Integrity (I)</label>
                            <Dropdown v-model="model.base_cvss.i" :options="cvssChoices.cia" optionLabel="title" optionValue="value" @change="patchCVSS({ i: this.model.base_cvss.i })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="av">Availability (A)</label>
                            <Dropdown v-model="model.base_cvss.a" :options="cvssChoices.cia" optionLabel="title" optionValue="value" @change="patchCVSS({ a: this.model.base_cvss.a })"></Dropdown>
                        </div>
                    </div>
                </div>
                <div class="grid">
                    <div class="col-12">
                        <ProgressBar :value="model.base_cvss.cvss31_base_score * 10">
                            {{ model.base_cvss.cvss31_base_score }}
                        </ProgressBar>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>