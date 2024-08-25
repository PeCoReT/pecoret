<script>
import UserService from '@/service/UserService';

export default {
    name: 'APITokenCreate',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                date_expire: null,
                scope_all_projects: 'No Access',
                scope_user: 'No Access',
                scope_companies: 'No Access',
                scope_attack_surface: 'No Access',
                scope_advisories: 'No Access',
                scope_knowledgebase: 'No Access'
            },
            loading: false,
            service: new UserService(),
            accessChoices: [
                {
                    label: 'No Access',
                    value: 'No Access'
                },
                {
                    label: 'Read',
                    value: 'Read'
                },
                {
                    label: 'Read Write',
                    value: 'Read Write'
                }
            ]
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        create() {
            this.service.createAPIToken(this.$api, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'API-Token created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="API-Token" outlined @click="open"></Button>

    <ModalDialog header="Create API-Token" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </Field>
            <Field label="Date Expire?">
                <DatePicker v-model="model.date_expire" id="date_expire"></DatePicker>
            </Field>
            <Field label="Scope All Projects?">
                <Select v-model="this.model.scope_all_projects" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Select>
            </Field>
            <Field label="Scope Companies?">
                <Select v-model="this.model.scope_companies" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Select>
            </Field>
            <Field label="Scope User?">
                <Select v-model="this.model.scope_user" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Select>
            </Field>
            <Field label="Scope Advisories?">
                <Select v-model="this.model.scope_advisories" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Select>
            </Field>
            <Field label="Scope Attack Surface?">
                <Select v-model="this.model.scope_attack_surface" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Select>
            </Field>
            <Field label="Scope Knowledge Base?">
                <Select v-model="this.model.scope_knowledgebase" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
