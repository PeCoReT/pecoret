<script>
export default {
    name: 'CVSS4CalculatorForm',
    props: {
        modelValue: {
            required: true
        }
    },
    watch: {
        modelValue: {
            deep: true,
            handler(newValue) {
                let refreshScore = false;
                if (newValue.vector !== this.vectorString) {
                    refreshScore = true;
                }
                this.vectorToObject(newValue.vector);
                if (refreshScore === true) {
                    let data = {
                        vector: this.vectorString
                    };
                    this.$api.post('/cvss-calculator/4.0/', data).then((response) => {
                        this.severity = response.data.severity;
                        this.score = response.data.score;
                        this.$emit('update:score', {
                            score: this.score,
                            severity: this.severity
                        });
                    });
                }
            }
        }
    },
    emits: ['update:modelValue', 'update:score'],
    data() {
        return {
            findingId: this.$route.params.findingId,
            projectId: this.$route.params.projectId,
            av: 'N',
            at: 'N',
            ac: 'L',
            pr: 'N',
            ui: 'N',
            vc: 'N',
            vi: 'N',
            va: 'N',
            sc: 'N',
            si: 'N',
            sa: 'N',
            score: 0.0,
            severity: 'Informational',
            avChoices: [
                {
                    label: 'Network',
                    value: 'N'
                },
                {
                    label: 'Adjacent',
                    value: 'A'
                },
                {
                    label: 'Local',
                    value: 'L'
                },
                {
                    label: 'Physical',
                    value: 'P'
                }
            ],
            acChoices: [
                {
                    label: 'Low',
                    value: 'L'
                },
                {
                    label: 'High',
                    value: 'H'
                }
            ],
            atChoices: [
                {
                    label: 'None',
                    value: 'N'
                },
                {
                    label: 'Present',
                    value: 'P'
                }
            ],
            prChoices: [
                {
                    label: 'None',
                    value: 'N'
                },
                {
                    label: 'Low',
                    value: 'L'
                },
                {
                    label: 'High',
                    value: 'H'
                }
            ],
            uiChoices: [
                {
                    label: 'None',
                    value: 'N'
                },
                {
                    label: 'Passive',
                    value: 'P'
                },
                {
                    label: 'Active',
                    value: 'A'
                }
            ],
            impactChoices: [
                {
                    label: 'High',
                    value: 'H'
                },
                {
                    label: 'Low',
                    value: 'L'
                },
                {
                    label: 'None',
                    value: 'N'
                }
            ]
        };
    },
    computed: {
        vectorString() {
            return `CVSS:4.0/AV:${this.av}/AC:${this.ac}/AT:${this.at}/PR:${this.pr}/UI:${this.ui}/VC:${this.vc}/VI:${this.vi}/VA:${this.va}/SC:${this.sc}/SI:${this.si}/SA:${this.sa}`;
        }
    },
    methods: {
        vectorToObject(value) {
            let regex =
                'CVSS:4\\.0\\/AV:(?<av>[N|A|L|P])\\/AC:(?<ac>[L|H])\\/AT:(?<at>[N|P])\\/PR:(?<pr>[N|L|H])\\/UI:(?<ui>' +
                '[N|P|A])\\/VC:(?<vc>[H|L|N])\\/VI:(?<vi>[H|L|N])\\/VA:(?<va>[H|L|N])\\/SC:(?<sc>[H|L|N])\\/SI:(?<si>' +
                '[H|L|N])\\/SA:(?<sa>[H|L|N])';
            let re = RegExp(regex).exec(value);
            if (re === null) {
                return;
            }
            let groups = re.groups;
            this.ac = groups.ac;
            this.av = groups.av;
            this.at = groups.at;
            this.pr = groups.pr;
            this.ui = groups.ui;
            this.vc = groups.vc;
            this.vi = groups.vi;
            this.va = groups.va;
            this.sc = groups.sc;
            this.si = groups.si;
            this.sa = groups.sa;
        },
        getScore() {
            let data = {
                vector: this.vectorString
            };
            this.$api.post('/cvss-calculator/4.0/', data).then((response) => {
                this.severity = response.data.severity;
                this.score = response.data.score;
                this.$emit('update:modelValue', {
                    score: this.score,
                    severity: this.severity,
                    vector: this.vectorString
                });
            });
            let url = `/projects/${this.projectId}/findings/${this.findingId}/`;
            this.$api.patch(url, { cvss_score_40: this.vectorString });
        }
    }
};
</script>

<template>
    <div class="grid formgrid p-fluid">
        <Card class="card surface-ground col-12">
            <template #title> Exploitability Metrics</template>
            <template #content>
                <div class="grid">
                    <div class="col-12 field">
                        <label for="av">Attack Vector (AV)</label>
                        <SelectButton v-model="av" :options="avChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label for="ac">Attack Complexity (AC)</label>
                        <SelectButton v-model="ac" :options="acChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label for="at">Attack Requirements (AT)</label>
                        <SelectButton v-model="at" :options="atChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label for="pr">Privileges Required (PR)</label>
                        <SelectButton v-model="pr" :options="prChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label for="ui">User Interaction (UI)</label>
                        <SelectButton v-model="ui" :options="uiChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                </div>
            </template>
        </Card>
        <Card class="surface-ground col-12 md:col-6 card h-full">
            <template #title>Vulnerable System Impact Metrics</template>
            <template #content>
                <div class="col-12 field">
                    <label for="vc">Confidentiality (VC)</label>
                    <SelectButton v-model="vc" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
                <div class="col-12 field">
                    <label for="vi">Integrity (VI)</label>
                    <SelectButton v-model="vi" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
                <div class="col-12 field">
                    <label for="va">Availability (VA)</label>
                    <SelectButton v-model="va" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
            </template>
        </Card>
        <Card class="surface-ground col-12 md:col-6 card h-full">
            <template #title>Subsequent System Impact Metrics</template>
            <template #content>
                <div class="col-12 field">
                    <label for="sc">Confidentiality (SC)</label>
                    <SelectButton v-model="sc" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
                <div class="col-12 field">
                    <label for="si">Integrity (SI)</label>
                    <SelectButton v-model="si" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
                <div class="col-12 field">
                    <label for="sa">Availability (SA)</label>
                    <SelectButton v-model="sa" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
            </template>
        </Card>
    </div>
</template>

<style scoped></style>