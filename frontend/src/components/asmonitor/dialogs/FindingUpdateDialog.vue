<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import ASMonitorService from '@/service/ASMonitorService';
import TagSelectField from '@/components/asmonitor/TagSelectField.vue';

export default {
    name: 'FindingUpdateDialog',
    components: { TagSelectField, ModalDialog },
    emits: ['object-updated'],

    props: {
        finding: {
            required: true
        },
        programId: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            loading: false,
            model: this.target,
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            this.loading = true;
            let data = {
                name: this.model.name,
                tags: this.model.tags
            };
            if (this.model.tags.length > 0 && this.model.tags[0].pk) {
                delete data.tags;
            }
            this.service
                .patchFinding(this.$api, this.programId, this.finding.pk, data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Finding updated!',
                        life: 3000,
                        detail: 'Finding updated successfully!'
                    });
                    this.$emit('object-updated');
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        finding: {
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
    <Button icon="fa fa-edit" label="Edit" outlined @click="open"></Button>
    <ModalDialog :loading="loading" header="Update Finding" v-model="showDialog" @onSave="patch">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText v-model="model.name" id="name"></InputText>
            </div>
            <div class="field col-12">
                <label for="tags">Tags</label>
                <TagSelectField v-model="model.tags"></TagSelectField>
            </div>
        </div>
    </ModalDialog>
</template>

<style scoped></style>
