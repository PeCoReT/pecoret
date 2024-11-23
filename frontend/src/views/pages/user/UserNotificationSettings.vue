<script>
import UserSettingsPageLayout from '@/layout/UserSettingsPageLayout.vue';

export default {
    name: 'UserNotificationSettings',
    components: { UserSettingsPageLayout },
    data() {
        return {
            model: {}
        };
    },
    methods: {
        getItem() {
            this.$api.get(this.$api.e.userUserSettings).then((response) => {
                this.model = response.data;
            });
        },
        patch(data) {
            this.$api.patch(this.$api.e.userUserSettings, data).then((response) => {
                this.model = response.data;
                this.$toast.add({
                    severity: 'success',
                    summary: 'Updated',
                    detail: 'Settings were updated successfully!',
                    life: 3000
                });
            });
        }
    },
    mounted() {
        this.getItem();
    }
};
</script>

<template>
    <UserSettingsPageLayout subheadline="Change your notification settings here!" headline="Notifications">
        <div class="pt-6 pb-6 shadow-md">
            <div class="flex items-center justify-between py-4">
                <div>
                    <h2 class="text-lg font-medium">Email on new critical findings?</h2>
                    <p class="text-sm text-gray-400">Receive notification mail when new critical finding is created in one of your projects.</p>
                </div>
                <div>
                    <label class="relative inline-flex items-center">
                        <ToggleSwitch v-model="model.notify_critical_findings" @change="this.patch({ notify_critical_findings: model.notify_critical_findings })"></ToggleSwitch>
                    </label>
                </div>
            </div>
        </div>
    </UserSettingsPageLayout>
</template>
