<script>

export default {
    name: 'LabelUpdateDialog',
    emits: ['object-updated'],
    props: {
        label: {
            required: true
        }
    },
    data() {
        return {
            visible: false,
            loading: false,
            model: {
                name: this.label.name,
                description: this.label.description,
                color: this.label.color
            },
        };
    },
    methods: {
        open() {
            this.visible = true;
        },
        patch() {
            if (this.model.color.startsWith('#') === false) {
                this.model.color = '#' + this.model.color;
            }
            let data = {
                name: this.model.name,
                description: this.model.description,
                color: this.model.color
            };

            this.$api.patch(this.$api.e.aLabelDetail, {pk: this.label.pk}, data).then((response) => {
                this.$emit('object-updated', response.data);
                this.visible = false;
            });
        }
    },
    watch: {
        label: {
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
    <Button icon="fa fa-pen-to-square" size="small" outlined @click="open"></Button>

    <ModalDialog header="Create Label" v-model="visible" :loading="loading" @onSave="patch">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name"></InputText>
            </Field>
            <Field label="Description">
                <InputText id="description" maxlength="254" v-model="model.description"></InputText>
            </Field>
            <Field label="Color">
                <ColorPicker v-model="model.color"></ColorPicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
