<script>
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';

export default {
    name: 'ScoreList',
    components: { FindingTabMenu },
    mounted() {
        this.getCVSS();
        this.getOWASP();
    },
    methods: {
        getCVSS() {
            this.service.getCVSSScore(this.$api, this.projectId, this.findingId).then((response) => {
                this.model.base_cvss = response.data;
            });
        },
        getOWASP() {
            this.service.getOWASPRiskRating(this.$api, this.projectId, this.findingId).then((response) => {
                this.model.owasp = response.data;
            });
        },
        patchCVSS(data) {
            this.service.patchCVSSScore(this.$api, this.projectId, this.findingId, this.model.base_cvss.pk, data).then((response) => {
                this.model.base_cvss = response.data;
            });
        },
        patchOWASP(data) {
            this.service.patchOWASPRiskRating(this.$api, this.projectId, this.findingId, this.model.owasp.pk, data).then((response) => {
                this.model.owasp = response.data;
            });
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
                },
                owasp: {
                    skill_level: null
                }
            },
            owaspChoices: {
                skillLevel: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Security penetration skills' },
                    { value: 3, title: 'Networking and programming skills' },
                    { value: 5, title: 'Advanced computer user' },
                    { value: 6, title: 'Some technical skills' },
                    { value: 9, title: 'No technical skills' }
                ],
                motive: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Low or no reward' },
                    { value: 4, title: 'Possible reward' },
                    { value: 9, title: 'High reward' }
                ],
                opportunity: [
                    { value: 0, title: 'Full access or expensive resources required' },
                    { value: 4, title: 'Special access or resources required' },
                    { value: 7, title: 'Some access or resources required' },
                    { value: 9, title: 'No access or resources required' }
                ],
                size: [
                    { value: 0, title: 'N/A' },
                    { value: 2, title: 'Developers or system administrators' },
                    { value: 4, title: 'Intranet users' },
                    { value: 5, title: 'Partners' },
                    { value: 6, title: 'Authenticated users' },
                    { value: 9, title: 'Anonymous internet users' }
                ],
                easeOfDiscovery: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Practically impossible' },
                    { value: 3, title: 'Difficult' },
                    { value: 7, title: 'Easy' },
                    { value: 9, title: 'Automated tools available' }
                ],
                easeOfExploit: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Theoretical' },
                    { value: 3, title: 'Difficult' },
                    { value: 7, title: 'Easy' },
                    { value: 9, title: 'Automated tools available' }
                ],
                awareness: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Unknown' },
                    { value: 4, title: 'Hidden' },
                    { value: 6, title: 'Obvious' },
                    { value: 9, title: 'Public knowledge' }
                ],
                intrusionDetection: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Active detection in application' },
                    { value: 3, title: 'Logged and reviewed' },
                    { value: 8, title: 'Logged without review' },
                    { value: 9, title: 'Not logged' }
                ],
                lossOfConfidentiality: [
                    { value: 0, title: 'N/A' },
                    { value: 2, title: 'Minimal non-sensitive data disclosed' },
                    { value: 6, title: 'Minimal critical data or extensive non-sensitive data disclosed' },
                    { value: 7, title: 'Extensive critical data disclosed' },
                    { value: 9, title: 'All data disclosed' }
                ],
                lossOfIntegrity: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Minimal slightly corrupted data' },
                    { value: 3, title: 'Minimal seriously corrupt data' },
                    { value: 5, title: 'Extensive slightly corrupt data' },
                    { value: 7, title: 'Extensive seriously corrupt data' },
                    { value: 9, title: 'All data totally corrupt' }
                ],
                lossOfAvailability: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Minimal secondary services interrupted' },
                    {
                        value: 5,
                        title: 'Minimal primary services interrupted or extensive secondary services interrupted'
                    },
                    { value: 7, title: 'Extensive primary services interrupted' },
                    { value: 9, title: 'All services completely lost' }
                ],
                lossOfAccountability: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Fully traceable' },
                    { value: 7, title: 'Possibly traceable' },
                    { value: 9, title: 'Completely anonymous' }
                ],
                financialDamage: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Less than the cost to fix the vulnerability' },
                    { value: 3, title: 'Minor effect on annual profit' },
                    { value: 7, title: 'Significant effect on annual profit' },
                    { value: 9, title: 'Bankruptcy' }
                ],
                reputationDamage: [
                    { value: 0, title: 'N/A' },
                    { value: 1, title: 'Minimal damage' },
                    { value: 4, title: 'Loss of major accounts' },
                    { value: 5, title: 'Loss of goodwill' },
                    { value: 9, title: 'Brand damage' }
                ],
                nonCompliance: [
                    { value: 0, title: 'N/A' },
                    { value: 2, title: 'Minor violation' },
                    { value: 5, title: 'Clear violation' },
                    { value: 7, title: 'High profile violation' }
                ],
                privacyViolation: [
                    { value: 0, title: 'N/A' },
                    { value: 3, title: 'One individual' },
                    { value: 5, title: 'Hundreds of people' },
                    { value: 7, title: 'Thousands of people' },
                    { value: 9, title: 'Millions of people' }
                ]
            },
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

            <div class="card mt-3">
                <p class="text-xl">OWASP Risk-Rating</p>

                <div class="grid">
                    <div class="col-6">
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Skill Level</label>
                            <Dropdown v-model="model.owasp.skill_level" :options="owaspChoices.skillLevel" optionLabel="title" optionValue="value" @change="patchOWASP({ skill_level: this.model.owasp.skill_level })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Motive</label>
                            <Dropdown v-model="model.owasp.motive" :options="owaspChoices.motive" optionLabel="title" optionValue="value" @change="patchOWASP({ motive: this.model.owasp.motive })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Opportunity</label>
                            <Dropdown v-model="model.owasp.opportunity" :options="owaspChoices.opportunity" optionLabel="title" optionValue="value" @change="patchOWASP({ opportunity: this.model.owasp.opportunity })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Size</label>
                            <Dropdown v-model="model.owasp.size" :options="owaspChoices.size" optionLabel="title" optionValue="value" @change="patchOWASP({ size: this.model.owasp.size })"></Dropdown>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Ease of Discovery</label>
                            <Dropdown v-model="model.owasp.ease_of_discovery" :options="owaspChoices.easeOfDiscovery" optionLabel="title" optionValue="value" @change="patchOWASP({ ease_of_discovery: this.model.owasp.ease_of_discovery })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Ease of Exploit</label>
                            <Dropdown v-model="model.owasp.ease_of_exploit" :options="owaspChoices.easeOfExploit" optionLabel="title" optionValue="value" @change="patchOWASP({ ease_of_exploit: this.model.owasp.ease_of_exploit })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Awareness</label>
                            <Dropdown v-model="model.owasp.awareness" :options="owaspChoices.awareness" optionLabel="title" optionValue="value" @change="patchOWASP({ awareness: this.model.owasp.awareness })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Intrusion Detection</label>
                            <Dropdown
                                v-model="model.owasp.intrusion_detection"
                                :options="owaspChoices.intrusionDetection"
                                optionLabel="title"
                                optionValue="value"
                                @change="patchOWASP({ intrusion_detection: this.model.owasp.intrusion_detection })"
                            ></Dropdown>
                        </div>
                    </div>
                </div>

                <div class="grid">
                    <div class="col-12">
                        <p>Likelihood Factors</p>
                        <ProgressBar v-if="model.owasp.likelihood_factors" :value="model.owasp.likelihood_factors[0] * 10">
                            {{ model.owasp.likelihood_factors[0] }}
                        </ProgressBar>
                    </div>
                </div>

                <div class="grid mt-3">
                    <div class="col-6">
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Loss of Confidentiality</label>
                            <Dropdown
                                v-model="model.owasp.loss_of_confidentiality"
                                :options="owaspChoices.lossOfConfidentiality"
                                optionLabel="title"
                                optionValue="value"
                                @change="patchOWASP({ loss_of_confidentiality: this.model.owasp.loss_of_confidentiality })"
                            ></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Loss of Availability</label>
                            <Dropdown
                                v-model="model.owasp.loss_of_availability"
                                :options="owaspChoices.lossOfAvailability"
                                optionLabel="title"
                                optionValue="value"
                                @change="patchOWASP({ loss_of_availability: this.model.owasp.loss_of_availability })"
                            ></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Loss of Integrity</label>
                            <Dropdown v-model="model.owasp.loss_of_integrity" :options="owaspChoices.lossOfIntegrity" optionLabel="title" optionValue="value" @change="patchOWASP({ loss_of_integrity: this.model.owasp.loss_of_integrity })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Loss of Accountability</label>
                            <Dropdown
                                v-model="model.owasp.loss_of_accountability"
                                :options="owaspChoices.lossOfAccountability"
                                optionLabel="title"
                                optionValue="value"
                                @change="patchOWASP({ loss_of_accountability: this.model.owasp.loss_of_accountability })"
                            ></Dropdown>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Financial Damage</label>
                            <Dropdown v-model="model.owasp.financial_damage" :options="owaspChoices.financialDamage" optionLabel="title" optionValue="value" @change="patchOWASP({ financial_damage: this.model.owasp.financial_damage })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Reputation Damage</label>
                            <Dropdown v-model="model.owasp.reputation_damage" :options="owaspChoices.reputationDamage" optionLabel="title" optionValue="value" @change="patchOWASP({ reputation_damage: this.model.owasp.reputation_damage })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Non-compliance</label>
                            <Dropdown v-model="model.owasp.non_compliance" :options="owaspChoices.nonCompliance" optionLabel="title" optionValue="value" @change="patchOWASP({ non_compliance: this.model.owasp.non_compliance })"></Dropdown>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="skill_level">Privacy Violation</label>
                            <Dropdown v-model="model.owasp.privacy_violation" :options="owaspChoices.privacyViolation" optionLabel="title" optionValue="value" @change="patchOWASP({ privacy_violation: this.model.owasp.privacy_violation })"></Dropdown>
                        </div>
                    </div>
                </div>

                <div class="grid">
                    <div class="col-12">
                        <p>Impact Factors</p>
                        <ProgressBar v-if="model.owasp.impact_factors" :value="model.owasp.impact_factors[0] * 10">
                            {{ model.owasp.impact_factors[0] }}
                        </ProgressBar>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>