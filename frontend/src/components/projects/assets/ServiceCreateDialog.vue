<script>

export default {
    name: 'ServiceCreateDialog',
    emits: ['object-created'],
    props: {
        projectId: {
            required: true
        },
        hostId: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            loading: false,
            model: {
                name: null,
                protocol: null,
                port: null,
                product: null,
                state: 'Open'
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
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.loading = true;
            this.model.host = this.hostId;
            this.$api
                .post(this.$api.e.pServiceList, { projectPk: this.projectId }, this.model)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Created!',
                        life: 3000,
                        detail: 'Service created!'
                    });
                    this.$emit('object-created', response.data);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Service" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" @onSave="create" v-model="showDialog" header="Create Service">
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
