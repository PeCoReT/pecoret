<script>
import { SeveritySelectField } from '@/partials/common';
import { Input } from '@/components/ui/input';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Select } from '@/components/select';
import { severityChoices } from '@/utils/constants';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'FindingCreate',
    components: {
        ContainerLayout,
        Select,
        ModelCombobox,
        Input,
        SeveritySelectField,
        Button,
        PageHeader
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            model: {
                vulnerability: null,
                severity: null,
                asset: null,
                authentication_required: false,
                user_account: null,
                name: null
            },
            loading: false
        };
    },
    methods: {
        severityChoices() {
            return severityChoices;
        },
        onTemplateChange(template) {
            this.model.severity = template.severity;
        },
        create() {
            this.loading = true;
            let data = {
                asset: this.model.asset,
                severity: this.model.severity,
                name: this.model.name,
                status: 'Open',
                vulnerability_id: this.model.vulnerability,
                user_account: this.model.user_account
            };
            this.$api.post(this.$api.e.pFindingList, { pPk: this.projectId }, data).then((response) => {
                this.$toaster({
                    title: 'Finding created!',
                    duration: 3000,
                    detail: 'Finding created successfully!'
                });
                this.$router.push({
                    name: 'FindingDetail',
                    params: {
                        projectId: this.projectId,
                        findingId: response.data.pk
                    }
                });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Create Finding</PageHeader>
        <Form>
            <Field label="Vulnerability">
                <ModelCombobox v-model="model.vulnerability" :api-endpoint="this.$api.e.pVulnerabilitySearch" :url-args="{ pPk: this.projectId }" label="" value-field="vulnerability_id" variant="form" @select="onTemplateChange"></ModelCombobox>
            </Field>
            <Field label="Name">
                <Input id="name" v-model="model.name" label="Name" type="text"></Input>
            </Field>
            <Field label="Severity">
                <Select v-model="model.severity" :options="severityChoices()"></Select>
            </Field>
            <Field label="Asset">
                <ModelCombobox v-model="model.asset" :api-endpoint="this.$api.e.pAssetList" :url-args="{ pPk: this.projectId }" label="" variant="form"></ModelCombobox>
            </Field>
            <Field label="Account">
                <ModelCombobox v-model="model.user_account" :api-endpoint="this.$api.e.pAccountList" label="" label-field="username" variant="form"></ModelCombobox>
            </Field>
            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </ContainerLayout>
</template>
