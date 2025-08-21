<script>
import { TechnologySelectField } from '@/partials/common';
import { ModalDialog } from '@/components/dialog';
import { Input } from '@/components/ui/input';

export default {
    name: 'FindingAsAdvisoryDialog',
    emits: ['object-created', 'update:modelValue'],
    props: ['modelValue'],
    data() {
        return {
            showDialog: this.modelValue,
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            loading: false,
            model: {
                technology: null,
                affected_versions: null
            }
        };
    },
    methods: {
        create() {
            this.loading = true;
            let data = {
                technology: this.model.technology,
                affected_versions: this.model.affected_versions
            };
            this.$api
                .post(this.$api.e.pFindingAsAdvisory, { pPk: this.projectId, pk: this.findingId }, data)
                .then((response) => {
                    this.$toaster({
                        title: 'Finding copies as advisory!',
                        duration: 3000,
                        description: 'Finding was successfully copied as advisory!'
                    });
                    this.$emit('object-created', response.data);
                    this.$emit('update:modelValue', false);
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        modelValue: {
            immediate: true,
            deep: true,
            handler(value) {
                this.showDialog = value;
            }
        }
    },
    components: { ModalDialog, TechnologySelectField, Input }
};
</script>

<template>
    <ModalDialog v-model="showDialog" v-model:loading="loading" header="Finding as Advisory" @onSave="create" @update:modelValue="this.$emit('update:modelValue')">
        <Form>
            <Field label="Product">
                <TechnologySelectField v-model="model.technology"></TechnologySelectField>
            </Field>
            <Field label="Affected Versions">
                <Input v-model="model.affected_versions"></Input>
            </Field>
        </Form>
    </ModalDialog>
</template>
