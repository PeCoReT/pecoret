<script>
export default {
    name: 'Settings',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Settings',
                    disabled: true
                }
            ],
            menuItems: [
                {
                    label: 'General',
                    command: () => {
                        this.getGeneralItems();
                    }
                },
                {
                    label: 'Advisories',
                    command: () => {
                        this.getItems('/settings/advisories/');
                    }
                }
            ],
            items: null
        };
    },
    methods: {
        getItems(url) {
            this.$api.get(url).then((response) => {
                this.items = response.data;
            });
        },
        getGeneralItems() {
            this.getItems('/settings/general/');
        },
        saveSettings(item) {
            let data = {
                setting_value: item.value
            };
            this.$api.patch(`/settings/${item.pk}/`, data).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Updated',
                    detail: 'Settings updated!',
                    life: 3000
                });
            });
        }
    },
    mounted() {
        this.getGeneralItems();
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
            <div class="card">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-2">
                        <Menu :model="menuItems" class="surface-ground w-20rem"></Menu>
                    </div>
                    <div class="col-span-10">
                        <Form>
                            <Field v-for="item in items" :key="item.pk" :label="item.name">
                                <InputNumber v-if="item.value_type === 'int'" v-model="item.value" :id="item.name" @change="saveSettings(item)"></InputNumber>
                                <InputText :id="item.name" v-model="item.value" v-else @change="saveSettings(item)"></InputText>
                                <small :id="item.name" v-if="item.description !== null && item.description !== ''">{{ item.description }}</small>
                            </Field>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
