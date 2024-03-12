<script>
import UserService from '@/service/UserService';

export default {
    name: 'APITokenCreate',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                date_expire: null,
                scope_all_projects: 'No Access',
                scope_user: 'No Access',
                scope_companies: 'No Access',
                scope_asmonitor: 'No Access',
                scope_advisories: 'No Access'
            },
            service: new UserService(),
            accessChoices: [
                {
                    label: 'No Access',
                    value: 'No Access'
                },
                {
                    label: 'Read',
                    value: 'Read'
                },
                {
                    label: 'Read Write',
                    value: 'Read Write'
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
        create() {
            this.service.createAPIToken(this.$api, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'API-Token created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="API-Token" outlined @click="open"></Button>

    <Dialog header="Create API-Token" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <label for="date_expire">Date Expire?</label>
                <Calendar v-model="model.date_expire" id="date_expire"></Calendar>
            </div>
            <div class="field col-12 md:col-6">
                <label for="scope_all_projects">Scope All Projects?</label>
                <Dropdown v-model="this.model.scope_all_projects" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Dropdown>
            </div>
            <div class="field col-12 md:col-6">
                <label for="scope_all_projects">Scope Companies?</label>
                <Dropdown v-model="this.model.scope_companies" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Dropdown>
            </div>
            <div class="field col-12 md:col-6">
                <label for="scope_all_projects">Scope User?</label>
                <Dropdown v-model="this.model.scope_user" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Dropdown>
            </div>
            <div class="field col-12 md:col-6">
                <label for="scope_all_projects">Scope Advisories?</label>
                <Dropdown v-model="this.model.scope_advisories" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="scope_asmonitor">Scope Attack Surface?</label>
                <Dropdown v-model="this.model.scope_asmonitor" :options="accessChoices" optionLabel="label" optionValue="value" class="w-full"></Dropdown>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
