<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TargetMetaCreateDialog from '@/components/asmonitor/dialogs/TargetMetaCreateDialog.vue';
import TargetDetailTabMenu from '@/components/asmonitor/TargetDetailTabMenu.vue';

export default {
    name: 'TargetDetail',
    components: { TargetDetailTabMenu, TargetMetaCreateDialog, MarkdownEditor, BaseLayout },
    data() {
        return {
            service: new ASMonitorService(),
            programId: this.$route.params.programId,
            targetId: this.$route.params.targetId,
            item: null,
            metas: null,
            selectedMeta: null,
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            breadcrumbs: [
                {
                    label: 'Hosts',
                    to: this.$router.resolve({
                        name: 'ASMonitorTargetList',
                        params: {
                            programId: this.$route.params.programId
                        }
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getItem();
        this.getTargetMeta();
    },
    methods: {
        getItem() {
            this.service.getTarget(this.$api, this.programId, this.targetId).then((resp) => {
                this.item = resp.data;
            });
        },
        getTargetMeta() {
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.service.getTargetMetas(this.$api, this.programId, this.targetId, params).then((resp) => {
                this.metas = resp.data.results;
                this.totalRecords = resp.data.count;
            });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getTargetMeta();
        },
        onMetaSelected(event) {
            if (event.value === null) {
                this.selectedMeta = null;
                return;
            }
            this.getTargetMeta();
            for (let i = 0; i < this.metas.length; i++) {
                if (this.metas[i].pk === event.value.pk) {
                    this.selectedMeta = this.metas[i];
                    break;
                }
            }
        },
        patchMeta() {
            let data = {
                value: this.selectedMeta.value
            };
            this.service.patchTargetMeta(this.$api, this.programId, this.targetId, this.selectedMeta.pk, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Meta data updated!',
                    detail: 'Target meta data updated successfully!',
                    life: 3000
                });
            });
        },
        onListFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getTargetMetas(this.$api, this.programId, this.targetId, params).then((response) => {
                this.notes = response.data.results;
            });
        },
        deleteMeta() {
            this.$confirm.require({
                message: 'Do you want to delete this item?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTargetMeta(this.$api, this.programId, this.targetId, this.selectedMeta.pk).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Item was deleted!',
                            life: 3000
                        });
                        this.getTargetMeta();
                        this.selectedMeta = null;
                    });
                }
            });
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #pre-content-right>
            <div class="flex justify-content-end">
                <TargetMetaCreateDialog @object-created="getTargetMeta"></TargetMetaCreateDialog>
                <Button icon="fa fa-trash" label="Delete" outlined severity="danger" @click="deleteMeta" :disabled="!selectedMeta"></Button>
            </div>
        </template>
        <template #default>
            <div class="col-12">
                <TargetDetailTabMenu class="surface-card"></TargetDetailTabMenu>
                <div class="card border-noround-top">
                    <div class="grid">
                        <div class="col-3 h-full">
                            <Listbox @change="onMetaSelected" v-model="selectedMeta" :options="metas" optionLabel="key" class="w-full" filter @filter="onListFilter">
                                <template #option="slotProps">
                                    {{ slotProps.option.key }}
                                </template>
                            </Listbox>
                            <Paginator :rows="pagination.limit" :totalRecords="totalRecords" @page="onPage"></Paginator>
                        </div>
                        <div class="col-9">
                            <div class="grid formgrid p-fluid">
                                <div class="col-12 field">
                                    <MarkdownEditor v-if="selectedMeta !== null" v-model="selectedMeta.value" @blur="patchMeta"></MarkdownEditor>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </BaseLayout>
</template>
