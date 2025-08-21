<script>
import { findingStatusChoices } from '@/utils/constants';
import { FindingTabMenu } from '@/partials/projects';
import { MarkdownEditor } from '@/components/editor';
import { Select } from '@/components/select';
import { DatePicker } from '@/components/datepicker';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'FindingRetest.vue',
    components: { ContainerLayout, FindingTabMenu, MarkdownEditor, Select, DatePicker, Button },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            this.$api.get(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.findingId }).then((response) => {
                this.finding = response.data;
                this.model.status = response.data.status;
                this.model.retest_results = response.data.retest_results;
                this.model.date_retest = response.data.date_retest;
            });
        },
        patchFinding() {
            this.loading = true;
            this.$api
                .patch(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.finding.pk }, this.model)
                .then(() => {
                    this.$toaster({
                        title: 'Finding updated!',
                        duration: 3000,
                        description: 'Finding was updated successfully!'
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    data() {
        return {
            findingId: this.$route.params.findingId,
            projectId: this.$route.params.projectId,
            loading: false,
            finding: { component: {} },
            model: {
                retest_results: null,
                date_retested: null,
                status: null
            },
            statusChoices: findingStatusChoices
        };
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <FindingTabMenu class="mb-3"></FindingTabMenu>
            <Form>
                <Field label="Status">
                    <Select v-model="model.status" :options="statusChoices" class="w-full"></Select>
                </Field>
                <Field label="Date Retested">
                    <DatePicker id="date_retested" v-model="model.date_retest"></DatePicker>
                </Field>
                <Field label="Retest Summary">
                    <MarkdownEditor id="retest" v-model="model.retest_results"></MarkdownEditor>
                </Field>
                <Button class="w-full" @click="patchFinding"> Save</Button>
            </Form>
        </template>
    </ContainerLayout>
</template>
