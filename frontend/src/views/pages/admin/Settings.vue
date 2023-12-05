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
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="grid">
                    <div class="col">
                        <Menu :model="menuItems" class="surface-ground w-20rem"></Menu>
                    </div>
                    <div class="col">
                        <div class="formgrid p-fluid grid">
                            <div class="col-12 field" v-for="item in items" :key="item.pk">
                                <label :for="item.name">{{ item.name }}</label>
                                <InputNumber v-if="item.value_type === 'int'" v-model="item.value" :id="item.name" @change="saveSettings(item)"></InputNumber>
                                <InputText :id="item.name" v-model="item.value" v-else @change="saveSettings(item)"></InputText>
                                <small :id="item.name" v-if="item.description !== null && item.description !== ''">{{ item.description }}</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
