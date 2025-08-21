<script>
import AlertPanel from '@/components/alert/Alert.vue';
import { useAuthStore } from '@/store/auth';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/select';
import { DatePicker } from '@/components/datepicker';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'APITokenCreate.vue',
    components: { ContainerLayout, AlertPanel, Input, Select, DatePicker, Button },
    data() {
        return {
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
            authStore: useAuthStore(),
            breadcrumbs: [
                {
                    label: 'API-Tokens',
                    route: this.$router.resolve({ name: 'APITokenList' })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            loading: false,
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
        create() {
            this.$api.post(this.$api.e.apiTokenList, null, this.model).then((response) => {
                this.$toaster({
                    title: 'Created!',
                    duration: 3000,
                    detail: 'API-Token created!'
                });
                this.authStore.setNewApiToken(response.data.token);
                this.$router.push({ name: 'APITokenList' });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout :breadcrumbs="breadcrumbs">
        <h3 class="text-3xl mb-3">Create API-Token</h3>
        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name" type="text"></Input>
            </Field>
            <Field label="Date Expire?">
                <DatePicker id="date_expire" v-model="model.date_expire"></DatePicker>
            </Field>
            <Field label="Scope All Projects?">
                <Select v-model="this.model.scope_all_projects" :options="accessChoices" class="w-full"></Select>
            </Field>
            <Field label="Scope Companies?">
                <Select v-model="this.model.scope_companies" :options="accessChoices" class="w-full"></Select>
            </Field>
            <Field label="Scope User?">
                <Select v-model="this.model.scope_user" :options="accessChoices" class="w-full"></Select>
            </Field>
            <Field label="Scope Advisories?">
                <Select v-model="this.model.scope_advisories" :options="accessChoices" class="w-full"></Select>
            </Field>
            <Field label="Scope Attack Surface?">
                <Select v-model="this.model.scope_attack_surface" :options="accessChoices" class="w-full"></Select>
            </Field>
            <Field label="Scope Knowledge Base?">
                <Select v-model="this.model.scope_knowledgebase" :options="accessChoices" class="w-full"></Select>
            </Field>
            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </ContainerLayout>

</template>
