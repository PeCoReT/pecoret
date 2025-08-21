<script>
import UserSettingsPageLayout from '@/layout/UserSettingsPageLayout.vue';
import { Input } from '@/components/ui/input';
import Select from '@/components/select/Select.vue';
import { Textarea } from '@/components/ui/textarea';
import InlineFieldGroup from '@/components/form/InlineFieldGroup.vue';
import InlineField from '@/components/form/InlineField.vue';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import PageHeader from '@/components/typography/PageHeader.vue';
import { Button } from '@/components/ui/button';

export default {
    name: 'WebhookUpdate',
    components: {
        PageHeader,
        Label,
        Switch,
        InlineField,
        InlineFieldGroup,
        Textarea,
        Select,
        UserSettingsPageLayout,
        Input,
        Button
    },
    data() {
        return {
            providerChoices: [
                {
                    label: 'Matrix.org',
                    value: 'matrix'
                },
                {
                    label: 'Generic',
                    value: 'generic'
                }
            ],
            model: {},
            webhookId: this.$route.params.webhookId
        };
    },
    mounted() {
        this.$api.get(this.$api.e.webhookDetail, { pk: this.webhookId }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        save() {
            let data = {
                name: this.model.name,
                provider: this.model.provider,
                secret: this.model.secret,
                url: this.model.url,
                additional_data: this.model.additional_data,
                event_new_target: this.model.event_new_target,
                event_critical_scan_finding: this.model.event_critical_scan_finding
            };
            this.$api.patch(this.$api.e.webhookDetail, { pk: this.webhookId }, data).then(() => {
                this.$router.push({
                    name: 'WebhookList'
                });
            });
        }
    }
};
</script>

<template>
    <UserSettingsPageLayout subheadline="Connect applications to PeCoReT" headline="Update Webhook">
        <Form>
            <Field label="Provider">
                <Select :options="providerChoices" v-model="model.provider"></Select>
            </Field>
            <Field label="URL">
                <Input id="url" type="url" v-model="model.url"></Input>
            </Field>
            <Field label="Secret">
                <Input id="secret" v-model="model.secret"></Input>
            </Field>
            <Field label="Additional Data">
                <Textarea v-model="model.additional_data"></Textarea>
                <small>Additional data in JSON format</small>
            </Field>
            <PageHeader>Events</PageHeader>
            <div class="flex flex-wrap gap-8">
                <div class="flex items-center space-x-2">
                    <Switch v-model:checked="model.event_new_target"></Switch>
                    <Label>New Target in Attack surface</Label>
                </div>
            </div>
            <div class="flex flex-wrap gap-8">
                <div class="flex items-center space-x-2">
                    <Switch v-model:checked="model.event_critical_scan_finding"></Switch>
                    <Label>New Scan Finding with Severity "Critical" in Attack Surface</Label>
                </div>
            </div>
            <Button class="w-full" @click="save">Save</Button>
        </Form>
    </UserSettingsPageLayout>
</template>
