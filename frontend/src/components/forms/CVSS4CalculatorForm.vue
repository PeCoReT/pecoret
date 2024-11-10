<script>
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';

export default {
    name: 'CVSS4CalculatorForm',
    components: { InlineFieldGroup },
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
                    this.$api.post(this.$api.e.cvss4Calc, null, data).then((response) => {
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
            this.$api.post(this.$api.e.cvss4Calc, null, data).then((response) => {
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
    <div class="grid grid-col-1">
        <div class="col-span-1 card">
            <h3 class="text-2xl">Exploitability Metrics</h3>
            <Form>
                <InlineFieldGroup>
                    <InlineField label="Attack Vector (AV)">
                        <SelectButton v-model="av" :options="avChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </InlineField>
                    <InlineField label="Attack Complexity (AC)">
                        <SelectButton v-model="ac" :options="acChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </InlineField>
                </InlineFieldGroup>
                <InlineFieldGroup>
                    <InlineField label="Attack Requirements (AT)">
                        <SelectButton v-model="at" :options="atChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </InlineField>
                    <InlineField label="Privileges Required (PR)">
                        <SelectButton v-model="pr" :options="prChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </InlineField>
                </InlineFieldGroup>
                <InlineFieldGroup>
                    <InlineField label="User Interaction (UI)">
                        <SelectButton v-model="ui" :options="uiChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                    </InlineField>
                </InlineFieldGroup>
            </Form>
        </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2">
        <div class="col-span-1 card h-full">
            <h3 class="text-2xl">Vulnerable System Impact Metrics</h3>
            <Form>
                <Field label="Confidentiality (VC)">
                    <SelectButton v-model="vc" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </Field>
                <Field label="Integrity (VI)">
                    <SelectButton v-model="vi" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </Field>
                <Field label="Availability (VA)">
                    <SelectButton v-model="va" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </Field>
            </Form>
        </div>
        <div class="col-span-1 card h-full">
            <h3 class="text-2xl">Subsequent System Impact Metrics</h3>
            <Form>
                <Field label="Confidentiality (SC)">
                    <SelectButton v-model="sc" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </Field>
                <Field label="Integrity (SI)">
                    <SelectButton v-model="si" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </Field>
                <Field label="Availability (SA)">
                    <SelectButton v-model="sa" :options="impactChoices" option-label="label" option-value="value" @change="getScore" :allow-empty="false"></SelectButton>
                </Field>
            </Form>
        </div>
    </div>
</template>

<style>
.p-togglebutton.p-component {
    flex-grow: 1;
}
</style>
