<script>
import ProjectService from '@/service/ProjectService';
import CompanyService from '@/service/CompanyService';

export default {
    name: 'ProjectContactCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            companyId: null,
            loading: false,
            model: {
                name: null,
                date_expire: null
            },
            projectService: new ProjectService(),
            companyService: new CompanyService(),
            contactChoices: []
        };
    },
    mounted() {
        this.projectService.getProject(this.projectId).then((response) => {
            this.companyId = response.data.company;
        });
    },
    methods: {
        open() {
            this.visible = true;
        },
        getContactChoices() {
            if (this.contactChoices) {
                return;
            }
            this.companyService.getContacts(this.companyId).then((response) => {
                this.contactChoices = response.data.results;
            });
        },
        onFilterContact(event) {
            let params = {
                search: event.value
            };
            this.companyService.getContacts(this.companyId, params).then((response) => {
                this.contactChoices = response.data.results;
            });
        },
        create() {
            let data = {
                contact: this.model.contact
            };
            this.projectService.createContact(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Contact added!',
                    life: 3000,
                    detail: 'Contact added to project!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Contact" outlined @click="open"></Button>

    <ModalDialog header="Add Contact" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="Contact">
                <Select id="contact" filter optionValue="pk" :optionLabel="(option) => option.first_name + ' ' + option.last_name" :options="contactChoices" v-model="model.contact" @filter="onFilterContact" @focus="getContactChoices"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
