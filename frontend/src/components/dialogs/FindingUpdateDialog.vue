<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
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
            userAccountChoices: []
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
            this.$api.get(this.$api.e.pAccountList, { projectPk: this.projectId }).then((response) => {
                this.userAccountChoices = response.data.results;
            });
        },
        create() {
            this.loading = true;
            let data = {
                exclude_from_report: this.model.exclude_from_report,
                name: this.model.name,
                recommendation: this.model.recommendation,
                entrypoint: this.model.entrypoint
            };
            if (this.model.user_account) {
                data['user_account'] = this.model.user_account.pk;
            } else {
                data['user_account'] = null;
            }
            this.$api
                .patch(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.finding.pk }, data)
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
        <Form>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
            </Field>
            <Field label="Entrypoint">
                <InputText type="text" v-model="model.entrypoint"></InputText>
            </Field>
            <Field label="Account">
                <Select :options="userAccountChoices" @focus="onUserAccountFocus" optionLabel="username" v-model="model.user_account" show-clear></Select>
            </Field>
            <Field>
                <div class="flex align-items-center">
                    <Checkbox v-model="model.exclude_from_report" :binary="true" />
                    <label class="ml-2"> Exclude from report? </label>
                </div>
            </Field>
            <Field label="Recommendation">
                <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
