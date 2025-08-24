<script>
import UserSettingsPageLayout from '@/layout/UserSettingsPageLayout.vue';
import AlertPanel from '@/components/alert/Alert.vue';
import { useAuthStore } from '@/store/auth';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/select';
import { DatePicker } from '@/components/datepicker';
import { Button } from '@/components/ui/button';
import PageHeader from '@/components/typography/PageHeader.vue';

export default {
    name: 'APITokenCreate',
    components: {
        UserSettingsPageLayout,
        AlertPanel,
        Input,
        Select,
        DatePicker,
        Button,
        PageHeader
    },
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
            loading: false,
            accessChoices: [
                { label: 'No Access', value: 'No Access' },
                { label: 'Read', value: 'Read' },
                { label: 'Read Write', value: 'Read Write' }
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
    <UserSettingsPageLayout subheadline="Manage your API tokens!" headline="API Tokens">
        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name" type="text" />
            </Field>

            <Field label="Date Expire?">
                <DatePicker id="date_expire" v-model="model.date_expire" />
            </Field>

            <PageHeader>Scopes</PageHeader>

            <Field label="All Projects">
                <Select v-model="model.scope_all_projects" :options="accessChoices" class="w-full" />
            </Field>

            <Field label="Companies">
                <Select v-model="model.scope_companies" :options="accessChoices" class="w-full" />
            </Field>

            <Field label="User">
                <Select v-model="model.scope_user" :options="accessChoices" class="w-full" />
            </Field>

            <Field label="Advisories">
                <Select v-model="model.scope_advisories" :options="accessChoices" class="w-full" />
            </Field>

            <Field label="Attack Surface">
                <Select v-model="model.scope_attack_surface" :options="accessChoices" class="w-full" />
            </Field>

            <Field label="Knowledge Base">
                <Select v-model="model.scope_knowledgebase" :options="accessChoices" class="w-full" />
            </Field>

            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </UserSettingsPageLayout>
</template>
