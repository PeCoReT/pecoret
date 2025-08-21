<script>
import { ToggleGroup } from '@/components/togglegroup';

export default {
    name: 'CVSS31CalculatorForm',
    components: { ToggleGroup },
    props: {
        modelValue: {
            required: true
        }
    },
    watch: {
        modelValue: {
            deep: true,
            immediate: true,
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
                    this.$api.post(this.$api.e.cvss3Calc, null, data).then((response) => {
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
            let regex = 'CVSS:3\\.1\\/AV:(?<av>[N|A|L|P])\\/AC:(?<ac>[L|H])\\/PR:(?<pr>[N|L|H])\\/UI:(?<ui>' + '[N|R])\\/S:(?<s>[U|C])\\/C:(?<c>[H|L|N])\\/I:(?<i>[H|L|N])\\/A:(?<a>[H|L|N])';
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
            this.$api.post(this.$api.e.cvss3Calc, null, data).then((response) => {
                this.severity = response.data.severity;
                this.score = response.data.score;
                this.$emit('update:modelValue', {
                    score: this.score,
                    severity: this.severity,
                    vector: this.vectorString
                });
            });
            let url = `/projects/${this.projectId}/findings/${this.findingId}/`;
            this.$api.patch(url, null, { cvss_score_31: this.vectorString });
        }
    }
};
</script>

<template>
    <div class="grid grid-col-1">
        <Card class="col-span-1">
            <h3 class="text-2xl mb-3">Exploitability Metrics</h3>
            <Form>
                <Field label="Attack Vector (AV)">
                    <ToggleGroup v-model="av" :options="avChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
                <InlineFieldGroup>
                    <InlineField label="Attack Complexity (AC)">
                        <ToggleGroup v-model="ac" :options="acChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                    <InlineField label="Privileges Required (PR)">
                        <ToggleGroup v-model="pr" :options="prChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                </InlineFieldGroup>
                <InlineFieldGroup>
                    <InlineField label="User Interaction (UI)">
                        <ToggleGroup v-model="ui" :options="uiChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                    <InlineField label="Scope (S)">
                        <ToggleGroup v-model="s" :options="sChoices" @update:modelValue="getScore"></ToggleGroup>
                    </InlineField>
                </InlineFieldGroup>
            </Form>
        </Card>
        <Card class="col-span-1 mt-3">
            <h3 class="text-2xl mb-3">Impact Metrics</h3>
            <Form>
                <Field label="Confidentiality (C)">
                    <ToggleGroup v-model="c" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
                <Field label="Integrity (I)">
                    <ToggleGroup v-model="i" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
                <Field label="Availability (A)">
                    <ToggleGroup v-model="a" :options="impactChoices" @update:modelValue="getScore"></ToggleGroup>
                </Field>
            </Form>
        </Card>
    </div>
</template>

<style scoped></style>
