<script>
import { ToggleGroup } from '@/components/togglegroup';

export default {
    name: 'CVSS4CalculatorForm',
    components: { ToggleGroup },
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
            this.$api.patch(url, null, { cvss_score_40: this.vectorString });
        }
    }
};
</script>

<template>
    <div class="grid grid-col-1">
        <Card class="col-span-1">
            <h3 class="text-2xl mb-3">Exploitability Metrics</h3>
            <Form>
                <InlineFieldGroup>
                    <InlineField label="Attack Vector (AV)">
                        <ToggleGroup v-model="av" :options="avChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                    <InlineField label="Attack Complexity (AC)">
                        <ToggleGroup v-model="ac" :options="acChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                </InlineFieldGroup>
                <InlineFieldGroup>
                    <InlineField label="Attack Requirements (AT)">
                        <ToggleGroup v-model="at" :options="atChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                    <InlineField label="Privileges Required (PR)">
                        <ToggleGroup v-model="pr" :options="prChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                </InlineFieldGroup>
                <InlineFieldGroup>
                    <InlineField label="User Interaction (UI)">
                        <ToggleGroup v-model="ui" :options="uiChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                </InlineFieldGroup>
            </Form>
        </Card>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
        <Card class="col-span-1 h-full">
            <h3 class="text-2xl">Vulnerable System Impact Metrics</h3>
            <Form>
                <Field label="Confidentiality (VC)">
                    <ToggleGroup v-model="vc" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
                <Field label="Integrity (VI)">
                    <ToggleGroup v-model="vi" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
                <Field label="Availability (VA)">
                    <ToggleGroup v-model="va" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
            </Form>
        </Card>
        <Card class="col-span-1 h-full">
            <h3 class="text-2xl mb-3">Subsequent System Impact Metrics</h3>
            <Form>
                <Field label="Confidentiality (SC)">
                    <ToggleGroup v-model="sc" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
                <Field label="Integrity (SI)">
                    <ToggleGroup v-model="si" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
                <Field label="Availability (SA)">
                    <ToggleGroup v-model="sa" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
            </Form>
        </Card>
    </div>
</template>

<style>
.p-togglebutton.p-component {
    flex-grow: 1;
}
</style>
