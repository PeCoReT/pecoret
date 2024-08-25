<script>
import SettingsTabMenu from '@/components/navigation/SettingsTabMenu.vue';

export default {
    name: 'UserSettingsDetail',
    components: { SettingsTabMenu },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Settings',
                    disabled: true
                }
            ],
            model: {}
        };
    },
    methods: {
        getItem() {
            let url = '/users/user-settings/';
            this.$api.get(url).then((response) => {
                this.model = response.data;
            });
        },
        patch() {
            let url = '/users/user-settings/';
            this.$api.patch(url, this.model).then((response) => {
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
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <SettingsTabMenu></SettingsTabMenu>
            <Card>
                <template #title>General</template>
                <template #content>
                    <div class="grid formgrid p-fluid">
                        <div class="field col-12">
                            <div class="flex align-items-center">
                                <Checkbox v-model="model.show_real_name_in_report" id="show_real_name_in_report" binary />
                                <label for="show_real_name_in_report" class="ml-2"> Show real name in report? </label>
                            </div>
                            <small class="text-color-secondary">If checked, show your first and last name in several reports. Otherwise use username.</small>
                        </div>
                    </div>
                </template>
            </Card>

            <Card class="mt-3">
                <template #title>Notifications</template>
                <template #content>
                    <div class="grid formgrid p-fluid">
                        <div class="field col-12">
                            <div class="flex align-items-center">
                                <Checkbox v-model="model.notify_critical_findings" id="notify_critical_findings" binary />
                                <label for="notify_critical_findings" class="ml-2"> Notify me on new critical findings? </label>
                            </div>
                            <small class="text-color-secondary">Receive notification mail when new critical finding is created in one of your projects.</small>
                        </div>
                    </div>
                </template>
            </Card>

            <div class="flex justify-content-end mt-3">
                <Button @click="patch" label="Save"></Button>
            </div>
        </div>
    </div>
</template>