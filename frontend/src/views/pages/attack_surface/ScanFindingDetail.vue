<script>
import { asFindingStatusChoices, severityChoices } from '@/utils/constants';
import { MarkdownEditor } from '@/components/editor';
import { Card, DetailCardWithIcon, InfoCardWithForm } from '@/components/card';
import { Select } from '@/components/select';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { DatePicker } from '@/components/datepicker';

export default {
    name: 'ScanFindingDetail',
    components: { ContainerLayout, MarkdownEditor, InfoCardWithForm, DetailCardWithIcon, Card, Select, Button, DatePicker },
    data() {
        return {
            finding: {},
            findingId: this.$route.params.findingId,
            breadcrumbs: [
                {
                    label: 'Scan Findings',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceScanFindingList'
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getFinding();
    },
    computed: {
        statusChoices() {
            return asFindingStatusChoices;
        }
    },
    methods: {
        severityChoices() {
            return severityChoices;
        },
        getFinding() {
            this.$api.get(this.$api.e.asScanFindingDetail, { pk: this.findingId }).then((response) => {
                this.finding = response.data;
            });
        },
        patchFindingData(data) {
            this.$api.patch(this.$api.e.asScanFindingDetail, { pk: this.findingId }, data).then(() => {
                this.getFinding();
                this.$toaster({ title: 'Updated', description: 'Finding updated!', duration: 3000 });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <div class="grid grid-cols-12 gap-3">
            <div class="col-span-12 md:col-span-3">
                <DetailCardWithIcon :text="finding.name + `(by ${finding.tool})`" icon="fa-fingerprint" title="Name"> </DetailCardWithIcon>
            </div>
            <div class="col-span-12 md:col-span-3">
                <InfoCardWithForm class="w-full" icon="fa-bookmark" title="Status">
                    <Select v-model="finding.status" :options="statusChoices" class="w-full" @update:modelValue="patchFindingData({ status: finding.status })"></Select>
                </InfoCardWithForm>
            </div>
            <div class="col-span-12 md:col-span-3">
                <InfoCardWithForm title="Ignore Until" icon="fa fa-ban">
                    <DatePicker v-model="finding.ignore_until" @update:model-value="patchFindingData({ ignore_until: finding.ignore_until })"></DatePicker>
                </InfoCardWithForm>
            </div>
            <div class="col-span-12 md:col-span-3">
                <DetailCardWithIcon :text="finding.severity" icon="fa fa-shield-halved" title="Severity"> </DetailCardWithIcon>
            </div>
        </div>
        <div class="grid grid-cols-12">
            <div class="col-span-12 py-3">
                <h3 class="text-lg">Component</h3>
                <p>{{ finding.affected_component }}</p>
            </div>
            <div class="col-span-12 py-3">
                <h3 class="text-lg">Result</h3>
                <div class="markdown-block">
                    <div v-html="finding.result_html"></div>
                </div>
            </div>
            <div class="col-span-12 py-3">
                <h3 class="text-lg">Full Output</h3>
                <pre v-if="finding.full_output" class="card"><code>{{ finding.full_output }}</code></pre>
                <div v-else>-</div>
            </div>
        </div>
        <Form class="mt-3">
            <Field label="Comment">
                <MarkdownEditor v-model="finding.comment"></MarkdownEditor>
            </Field>
            <Button class="w-full" @click="patchFindingData({ comment: finding.comment })">Save</Button>
        </Form>
    </ContainerLayout>
</template>
