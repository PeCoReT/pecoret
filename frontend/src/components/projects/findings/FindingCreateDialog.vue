<script>
import FindingService from '@/service/FindingService';
import ProjectVulnerabilityAutocompleteField from '@/components/elements/forms/ProjectVulnerabilityAutocompleteField.vue';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';
import AssetSelectField from '@/components/elements/forms/AssetSelectField.vue';
import UserAccountService from '@/service/UserAccountService';

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
            service: new FindingService(),
            userAccountChoices: [],
            accountService: new UserAccountService()
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
            this.accountService.getAccounts(this.$api, this.projectId).then((response) => {
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
            this.service.createFinding(this.$api, this.projectId, data).then((response) => {
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
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <ProjectVulnerabilityAutocompleteField v-model="model.vulnerability" @update:severity="onVulnerabilitySeverityChange($event)"></ProjectVulnerabilityAutocompleteField>
            </div>
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
            </div>
            <div class="field col-12">
                <SeveritySelectField v-model="model.severity"></SeveritySelectField>
            </div>
            <AssetSelectField v-model="model.component"></AssetSelectField>
            <div class="field col-12">
                <label for="account">Account</label>
                <Dropdown :options="userAccountChoices" @focus="onUserAccountFocus" optionLabel="username" v-model="model.user_account"></Dropdown>
            </div>
        </div>
    </ModalDialog>
</template>
