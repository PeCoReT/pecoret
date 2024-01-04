<script>
import ProjectVulnerabilityAutocompleteField from '@/components/elements/forms/ProjectVulnerabilityAutocompleteField.vue';
import UserAccountService from '@/service/UserAccountService';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';
import AssetSelectField from '@/components/elements/forms/AssetSelectField.vue';
import FindingService from '@/service/FindingService';

export default {
    name: 'FindingCreate',
    methods: {
        onUserAccountFocus() {
            if (this.userAccountChoices.length) {
                return;
            }
            this.accountService.getAccounts(this.$api, this.projectId).then((response) => {
                this.userAccountChoices = response.data.results;
            });
        },
        onVulnerabilitySeverityChange(event) {
            this.model.severity = event;
        },
        createFinding() {
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
            this.service
                .createFinding(this.$api, this.projectId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Finding created!',
                        life: 3000,
                        detail: 'Finding was created successfully!'
                    });
                    this.$router.push({
                        name: 'FindingDetail',
                        params: {
                            projectId: this.projectId,
                            findingId: response.data.pk
                        }
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'FindingList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            model: {
                vulnerability: null,
                severity: null,
                component: null,
                authentication_required: false,
                user_account: null
            },
            loading: false,
            userAccountChoices: [],
            accountService: new UserAccountService(),
            service: new FindingService(),
            projectId: this.$route.params.projectId
        };
    },
    components: { ProjectVulnerabilityAutocompleteField, SeveritySelectField, AssetSelectField }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <Card>
                <template #content>
                    <div class="p-fluid grid formgrid">
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
                    <div class="flex flex-column gap-2 mt-3">
                        <div class="flex justify-content-end">
                            <Button label="Save" :loading="loading" @click="createFinding"></Button>
                        </div>
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>
