<script>
import ContributorService from '@/service/ContributorService';

export default {
    name: 'ContributorCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                user: null,
                role: null,
                active_until: null
            },
            loading: false,
            userChoices: [],
            roleChoices: [{ label: 'Project Leader' }, { label: 'Owner' }, { label: 'Read Only' }, { label: 'Contributor' }],
            contributorService: new ContributorService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        onFocusUser(event) {
            let url = '/users/';
            this.$api.get(url).then((response) => {
                this.userChoices = response.data.results;
            });
        },
        onFilterUser(event) {
            let url = '/users/';
            let config = {
                search: event.value
            };
            this.$api.get(url).then((response) => {
                this.userChoices = response.data.results;
            });
        },
        create() {
            let data = {
                role: this.model.role,
                active_until: this.model.active_until,
                user: this.model.user
            };
            this.contributorService.createContributor(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'User added!',
                    life: 3000,
                    detail: 'User added to project!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Member" outlined @click="open"></Button>

    <ModalDialog header="Add Member to Project" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="User">
                <Select v-model="model.user" optionLabel="username" id="user" :options="userChoices" optionValue="pk" @focus="onFocusUser" filter @filter="onFilterUser"></Select>
            </Field>
            <Field label="Role">
                <Select v-model="model.role" :options="roleChoices" optionValue="label" optionLabel="label"></Select>
            </Field>
            <Field label="Membership Expiry?">
                <DatePicker v-model="model.active_until"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
