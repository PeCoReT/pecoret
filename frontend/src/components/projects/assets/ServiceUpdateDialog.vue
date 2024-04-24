<script>
import AssetService from '@/service/AssetService';


export default {
    name: 'ServiceUpdateDialog',
    props: {
        asset: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.asset,
            service: new AssetService(),
            host: null,
            hosts: [],
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
        patch() {
            let data = {
                name: this.model.name,
                host: this.host,
                protocol: this.model.protocol,
                port: this.model.port,
                product: this.model.product,
                state: this.model.state
            };
            this.service.patchService(this.$api, this.$route.params.projectId, this.asset.pk, data).then(() => {
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        },
        onHostSelectFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getHosts(this.$api, this.projectId, params).then((response) => {
                this.hosts = response.data.results;
            });
        }
    },
    watch: {
        asset: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
                if (value.host) {
                    this.hosts.push(value.host);
                    this.host = value.host.pk;
                }
            }
        }
    },
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined label="Edit"></Button>

    <Dialog header="Update Service" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="host">Host</label>
                <Dropdown :options="hosts" optionLabel="name" optionValue="pk" id="host" filter v-model="host" @filter="onHostSelectFilter"></Dropdown>
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
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
