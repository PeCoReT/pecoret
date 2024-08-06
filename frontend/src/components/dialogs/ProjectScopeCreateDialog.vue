<script>
import ProjectScopeService from "@/service/ProjectScopeService";


export default {
    name: "ProjectScopeCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                details: null,
                permission: null
            },
            service: new ProjectScopeService(),
            permissionChoices: [
                {
                    label: "Allowed", value: "Allowed"
                },
                {
                    label: "Denied", value: "Denied"
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
            let data = {
                details: this.model.details,
                permission: this.model.permission
            };
            this.service.createScope(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "Scope Created!",
                    life: 3000,
                    detail: "Scope created successfully!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Scope" outlined @click="open"></Button>

    <Dialog header="Create Scope" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="formgrid grid p-fluid">
            <div class="field col-12">
                <label for="details">Details</label>
                <InputText v-model="model.details"></InputText>
            </div>
            <div class="field col-12">
                <label for="permission">Permission</label>
                <Dropdown option-label="label" option-value="value" v-model="model.permission"
                          :options="permissionChoices"></Dropdown>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>