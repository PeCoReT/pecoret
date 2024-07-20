<script>
import ReportService from '@/service/ReportService';
import ReportTemplateSelectField from "@/components/elements/forms/ReportTemplateSelectField.vue";

export default {
    name: 'ReportCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                template: null,
                author: null
            },
            templateChoices: null,
            authorChoices: null,
            loading: false,
            service: new ReportService()
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
            let data = {
                name: this.model.name,
                template: this.model.template,
                author: null
            };
            this.service
                .createReport(this.$api, this.projectId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Report created!',
                        life: 3000,
                        detail: 'New report created!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
    },
    components: {ReportTemplateSelectField}
};
</script>

<template>
    <Button icon="fa fa-plus" label="Report" outlined @click="open"></Button>

    <Dialog header="Create Report" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <ReportTemplateSelectField v-model="model.template"></ReportTemplateSelectField>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" :loading="loading" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>