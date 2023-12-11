<script>
export default {
    name: 'CVSS31CalculatorForm',
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
                    this.$api.post('/cvss-calculator/3.1/', data).then((response) => {
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
            ac: 'L',
            pr: 'N',
            ui: 'N',
            s: 'U',
            c: 'N',
            i: 'N',
            a: 'N',
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
                    label: 'Required',
                    value: 'R'
                }
            ],
            sChoices: [
                {
                    label: 'Unchanged',
                    value: 'U'
                },
                {
                    label: 'Changed',
                    value: 'C'
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
            return `CVSS:3.1/AV:${this.av}/AC:${this.ac}/PR:${this.pr}/UI:${this.ui}/S:${this.s}/C:${this.c}/I:${this.i}/A:${this.a}`;
        }
    },
    methods: {
        vectorToObject(value) {
            let regex =
                'CVSS:3\\.1\\/AV:(?<av>[N|A|L|P])\\/AC:(?<ac>[L|H])\\/PR:(?<pr>[N|L|H])\\/UI:(?<ui>' +
                '[N|R])\\/S:(?<s>[U|C])\\/C:(?<c>[H|L|N])\\/I:(?<i>[H|L|N])\\/A:(?<a>[H|L|N])';
            let re = RegExp(regex).exec(value);
            if (re === null) {
                return;
            }
            let groups = re.groups;
            this.ac = groups.ac;
            this.av = groups.av;
            this.pr = groups.pr;
            this.ui = groups.ui;
            this.c = groups.c;
            this.i = groups.i;
            this.a = groups.a;
            this.s = groups.s;
        },
        getScore() {
            let data = {
                vector: this.vectorString
            };
            this.$api.post('/cvss-calculator/3.1/', data).then((response) => {
                this.severity = response.data.severity;
                this.score = response.data.score;
                this.$emit('update:modelValue', {
                    score: this.score,
                    severity: this.severity,
                    vector: this.vectorString
                });
            });
            let url = `/projects/${this.projectId}/findings/${this.findingId}/`;
            this.$api.patch(url, { cvss_score_31: this.vectorString });
        }
    }
};
</script>

<template>
    <div class="grid formgrid p-fluid">
        <Card class="card surface-ground col-12">
            <template #title>Exploitability Metrics</template>
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
                        <label for="pr">Privileges Required (PR)</label>
                        <SelectButton v-model="pr" :options="prChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label for="ui">User Interaction (UI)</label>
                        <SelectButton v-model="ui" :options="uiChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                    <div class="col-12 md:col-6 field">
                        <label for="s">Scope (S)</label>
                        <SelectButton v-model="s" :options="sChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </div>
                </div>
            </template>
        </Card>
        <Card class="surface-ground col-12 md:col-12 card h-full">
            <template #title>Impact Metrics</template>
            <template #content>
                <div class="col-12 field">
                    <label for="c">Confidentiality (C)</label>
                    <SelectButton v-model="c" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
                <div class="col-12 field">
                    <label for="i">Integrity (I)</label>
                    <SelectButton v-model="i" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
                <div class="col-12 field">
                    <label for="a">Availability (A)</label>
                    <SelectButton v-model="a" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </div>
            </template>
        </Card>
    </div>
</template>

<style scoped></style>