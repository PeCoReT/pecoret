<script>
import AssetService from '@/service/AssetService';


export default {
    name: 'ServiceCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                host: null,
                name: null,
                protocol: null,
                port: null,
                product: null,
                state: 'Open',
            },
            protocolChoices: [
                {
                    label: 'TCP',
                    value: 'TCP'
                },
                {
                    label: 'UDP',
                    value: 'UDP'
                }
            ],
            stateChoices: [
                {
                    label: 'Open',
                    value: 'Open'
                },
                {
                    label: 'Closed',
                    value: 'Closed'
                },
                {
                    label: 'Filtered',
                    value: 'Filtered'
                }
            ],
            hosts: [],
            service: new AssetService()
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
            this.loading = true;
            this.service
                .createService(this.$api, this.projectId, this.model)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Created!',
                        life: 3000,
                        detail: 'Service created!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onHostSelectFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getHosts(this.$api, this.projectId, params).then((response) => {
                this.hosts = response.data.results;
            });
        },
        onHostSelectFocus() {
            if (this.hosts.length > 0) {
                return;
            }
            this.service.getHosts(this.$api, this.projectId).then((response) => {
                this.hosts = response.data.results;
            });
        }
    },
};
</script>

<template>
    <Button icon="fa fa-plus" label="Service" outlined @click="open"></Button>

    <Dialog header="Create Service" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="host">Host</label>
                <Dropdown :options="hosts" optionLabel="name" optionValue="pk" id="host" filter @focus="onHostSelectFocus" v-model="model.host" @filter="onHostSelectFilter"></Dropdown>
            </div>
            <div class="field col-12 md:col-6">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="port">Port</label>
                <InputText id="port" type="text" v-model="model.port"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="protocol">Protocol</label>
                <Dropdown :options="protocolChoices" optionLabel="label" optionValue="value" id="protocol" type="text" v-model="model.protocol"></Dropdown>
            </div>
            <div class="field col-12 md:col-6">
                <label for="product">Product</label>
                <InputText id="product" type="text" v-model="model.product"></InputText>
            </div>
            <div class="field col-12 md:col-12">
                <label for="state">State</label>
                <Dropdown :options="stateChoices" optionLabel="label" optionValue="value" id="state" type="text" v-model="model.state"></Dropdown>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" :loading="loading" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
