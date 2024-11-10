<script>
import ProjectVulnerabilityAutocompleteField from '@/components/forms/fields/ProjectVulnerabilityAutocompleteField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import SeveritySelectField from '@/components/forms/fields/SeveritySelectField.vue';
import AssetSelectField from '@/components/forms/fields/AssetSelectField.vue';

export default {
    name: 'FindingCreateDialog',
    components: { ModalDialog, ProjectVulnerabilityAutocompleteField, SeveritySelectField, AssetSelectField },
    props: {
        projectId: {
            required: true
        }
    },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                vulnerability: null,
                severity: null,
                component: null,
                authentication_required: false,
                user_account: null,
                name: null
            },
            loading: false,
            userAccountChoices: []
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        onVulnerabilitySeverityChange(event) {
            this.model.severity = event;
        },
        onUserAccountFocus() {
            if (this.userAccountChoices.length) {
                return;
            }
            this.$api.get(this.$api.e.pAccountList, { projectPk: this.projectId }).then((response) => {
                this.userAccountChoices = response.data.results;
            });
        },
        create() {
            this.loading = true;
            let data = {
                component: this.model.component,
                severity: this.model.severity,
                name: this.model.name,
                status: 'Open',
                vulnerability_id: this.model.vulnerability
            };
            if (this.model.user_account) {
                data['user_account'] = this.model.user_account.pk;
            }
            if (this.model.severity && this.model.severity.value) {
                data['severity'] = this.model.severity.value;
            }
            this.$api.post(this.$api.e.pFindingList, { pPk: this.projectId }, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Finding created!',
                    life: 3000,
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
    <Button icon="fa fa-plus" label="Finding" outlined @click="open"></Button>
    <ModalDialog @onSave="create" header="New Finding" v-model="showDialog" v-model:loading="loading">
        <Form>
            <Field label="Vulnerability">
                <ProjectVulnerabilityAutocompleteField v-model="model.vulnerability" @update:severity="onVulnerabilitySeverityChange($event)"></ProjectVulnerabilityAutocompleteField>
            </Field>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
            </Field>
            <Field label="Severity">
                <SeveritySelectField v-model="model.severity"></SeveritySelectField>
            </Field>
            <AssetSelectField v-model="model.component"></AssetSelectField>
            <Field label="Account">
                <Select :options="userAccountChoices" @focus="onUserAccountFocus" optionLabel="username" v-model="model.user_account"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
