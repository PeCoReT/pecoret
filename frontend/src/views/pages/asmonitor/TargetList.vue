<script>
import ASMonitorService from '@/service/ASMonitorService';
import BlankSlate from '@/components/BlankSlate.vue';
import TargetCreateDialog from '@/components/asmonitor/TargetCreateDialog.vue';
import TargetUpdateDialog from '@/components/asmonitor/TargetUpdateDialog.vue';
import TagBadgeButton from '@/components/asmonitor/TagBadgeButton.vue';

export default {
    name: 'TargetList',
    components: { TargetUpdateDialog, TargetCreateDialog, BlankSlate, TagBadgeButton },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Targets',
                    disabled: true
                }
            ],
            service: new ASMonitorService(),
            items: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            tagChoices: [],
            programId: this.$route.params.programId,
            filters: {
                tags: { value: null }
            }
        };
    },
    methods: {
        onSort(event) {
            this.loading = true;
            let params = {
                ordering: event.sortField,
                tags: this.filters.tags.value
            };
            if (event.sortOrder === -1) {
                params['ordering'] = `-${event.sortField}`;
            }
            this.service
                .getTargets(this.$api, this.programId, params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getItems() {
            this.loading = true;
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page,
                tags: this.filters.tags.value
            };
            this.service
                .getTargets(this.$api, this.programId, data)
                .then((response) => {
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getTargets(this.$api, this.programId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        tagFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getTags(this.$api, params).then((response) => {
                this.tagChoices = response.data.results;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this target?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTarget(this.$api, this.programId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Target was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    mounted() {
        this.getItems();
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs" />
        </div>
    </div>
    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <TargetCreateDialog @object-created="getItems"></TargetCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    :paginator="true"
                    dataKey="pk"
                    :rowHover="this.items.length > 0"
                    :rows="pagination.limit"
                    :value="items"
                    :loading="loading"
                    :lazy="true"
                    :totalRecords="totalRecords"
                    @page="onPage"
                    filterDisplay="menu"
                    @filter="getItems"
                    v-model:filters="filters"
                    @sort="onSort"
                    removable-sort
                >
                    <template #empty>
                        <BlankSlate title="No targets!" text="No targets found!" icon="fa fa-crosshairs"></BlankSlate>
                    </template>
                    <template #header>
                        <div class="grid">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <Column field="name" header="Name" sortable></Column>
                    <Column field="ip" header="IP"></Column>
                    <Column field="last_seen" header="Last Seen" sortable>
                        <template #body="slotProps">
                            {{ slotProps.data.last_seen || 'Unknown' }}
                        </template>
                    </Column>
                    <Column field="tags" header="Tags" :showFilterMatchModes="false">
                        <template #body="slotProps">
                            <TagBadgeButton :label="tag" v-for="tag in slotProps.data.tags" :key="tag.pk"></TagBadgeButton>
                        </template>
                        <template #filter="{ filterModel }">
                            <MultiSelect v-model="filterModel.value" :options="tagChoices" @filter="tagFilter" placeholder="Select tags" filter @focus="tagFilter" class="p-column-filter" showClear optionLabel="name" optionValue="pk"></MultiSelect>
                        </template>
                    </Column>
                    <Column field="date_updated" header="Updated" sortable></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <TargetUpdateDialog :target="slotProps.data" @object-updated="getItems"></TargetUpdateDialog>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
