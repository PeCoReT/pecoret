<script>

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
            showDialog: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: this.asset,
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
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                protocol: this.model.protocol,
                port: this.model.port,
                product: this.model.product,
                state: this.model.state
            };
            this.$api.patch(this.$api.e.pServiceDetail, { projectPk: this.projectId, pk: this.asset.pk }, data).then(() => {
                this.$emit('object-updated', this.model);
                this.showDialog = false;
            });
        }
    },
    watch: {
        asset: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <ModalDialog header="Update Service" v-model="showDialog" v-model:loading="loading" @onSave="patch">
        <Form>
            <InlineFieldGroup>
                <InlineField label="Name">
                    <InputText id="name" type="text" v-model="model.name"></InputText>
                </InlineField>
                <InlineField label="Port">
                    <InputText id="port" type="text" v-model="model.port"></InputText>
                </InlineField>
            </InlineFieldGroup>
            <InlineFieldGroup>
                <InlineField label="Protocol">
                    <Select :options="protocolChoices" optionLabel="label" optionValue="value" id="protocol" type="text" v-model="model.protocol"></Select>
                </InlineField>
                <InlineField label="Product">
                    <InputText id="product" type="text" v-model="model.product"></InputText>
                </InlineField>
            </InlineFieldGroup>
            <Field label="State">
                <Select :options="stateChoices" optionLabel="label" optionValue="value" id="state" type="text" v-model="model.state"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
