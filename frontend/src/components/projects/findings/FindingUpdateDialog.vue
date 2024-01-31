<script>
import FindingService from '@/service/FindingService';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import UserAccountService from '@/service/UserAccountService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'FindingUpdateDialog',
    components: { ModalDialog, MarkdownEditor },
    props: {
        projectId: {
            required: true
        },
        finding: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            showDialog: false,
            model: this.finding,
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
                exclude_from_report: this.model.exclude_from_report,
                name: this.model.name,
                recommendation: this.model.recommendation
            };
            if (this.model.user_account) {
                data['user_account'] = this.model.user_account.pk;
            } else {
                data['user_account'] = null;
            }
            this.service
                .patchFinding(this.$api, this.projectId, this.finding.pk, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Finding updated!',
                        life: 3000,
                        detail: 'Finding updated successfully!'
                    });
                    this.$emit('object-updated', response.data);
                })
                .finally(() => {
                    this.loading = false;
                    this.showDialog = false;
                });
        }
    },
    watch: {
        finding: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
                if (value.user_account && value.user_account.pk) {
                    this.userAccountChoices = [value.user_account];
                }
            }
        }
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" label="Edit" outlined @click="open"></Button>
    <ModalDialog @onSave="create" header="Update Finding" v-model="showDialog" v-model:loading="loading">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
            </div>
            <div class="field col-12">
                <label for="account">Account</label>
                <Dropdown :options="userAccountChoices" @focus="onUserAccountFocus" optionLabel="username" v-model="model.user_account" show-clear></Dropdown>
            </div>
            <div class="field col-12">
                <label for="recommendation">Recommendation</label>
                <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>
