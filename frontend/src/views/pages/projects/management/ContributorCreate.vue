<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/select';
import { DatePicker } from '@/components/datepicker';

export default {
    name: 'ContributorCreate',
    components: { Button, ModelCombobox, BaseLayout, Select, DatePicker },
    data() {
        return {
            model: {
                role: null,
                user: null,
                active_until: null
            },
            projectId: this.$route.params.projectId,
            roleChoices: [
                {
                    label: 'Project Leader',
                    value: 'Project Leader'
                },
                { label: 'Owner', value: 'Owner' },
                { label: 'Read Only', value: 'Read Only' },
                { label: 'Contributor', value: 'Contributor' }
            ]
        };
    },
    methods: {
        create() {
            let data = {
                role: this.model.role,
                active_until: this.model.active_until,
                user: this.model.user
            };
            this.$api.post(this.$api.e.pMembershipList, { projectPk: this.projectId }, data).then((response) => {
                this.$toaster({
                    title: 'User added!',
                    duration: 3000,
                    detail: 'User added to project!'
                });
                this.$emit('object-created', response.data);
                this.$router.push({ name: 'ContributorList', params: { projectId: this.projectId } });
            });
        }
    }
};
</script>

<template>
    <BaseLayout>
        <Card class="col-span-12">
            <Form>
                <Field label="User">
                    <ModelCombobox v-model="model.user" :api-endpoint="this.$api.e.userList" label="Select user" label-field="username" value-field="pk">
                        <template #trigger="{ label }">
                            <Button class="justify-between text-muted-foreground" role="combobox" variant="outline">
                                {{ model.user ? label : 'Select user' }}
                                <i class="ml-2 h-4 w-4 shrink-0 opacity-50 fa fa-chevron-down" />
                            </Button>
                        </template>
                    </ModelCombobox>
                </Field>
                <Field label="Role">
                    <Select v-model="model.role" :options="roleChoices"></Select>
                </Field>
                <Field label="Membership Expiry?">
                    <DatePicker v-model="model.active_until"></DatePicker>
                </Field>
                <Button class="w-full" @click="create">Save</Button>
            </Form>
        </Card>
    </BaseLayout>
</template>
