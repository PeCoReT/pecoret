<script>
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { listViewMixin } from '@/mixins/listViewMixin';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import ScopeListSidebar from '@/partials/attack_surface/ScopeListSidebar.vue';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Button } from '@/components/ui/button';
import Search from '@/views/pages/attack_surface/Search.vue';
import SearchField from '@/partials/common/SearchField.vue';
import ScopeItemCreateForm from '@/partials/attack_surface/ScopeItemCreateForm.vue';
import PageHeader from '@/components/typography/PageHeader.vue';
import ScopeCreateForm from '@/partials/attack_surface/ScopeCreateForm.vue';
import { Paginator } from '@/components/paginator';

export default {
    name: 'ScopeList',
    components: {
        Paginator,
        ScopeCreateForm,
        PageHeader,
        ScopeItemCreateForm,
        SearchField,
        Search,
        ModelCombobox,
        ScopeListSidebar,
        DataViewContent,
        DataViewListLayout,
        ContainerLayout,
        Button
    },
    mixins: [listViewMixin],
    mounted() {},
    data() {
        return {
            items: [],
            filters: {
                scope: { value: null },
                search: { value: null }
            },
            reloadSidebar: false,
            loading: false,
            program: this.$route.query.program || null,
            showItemCreateForm: false,
            showScopeCreateForm: false
        };
    },
    methods: {
        sidebarChanged(item) {
            this.filters.scope.value = item.pk;
            this.getItems();
        },
        scopeItemDelete(pk) {
            this.$confirm.require({
                accept: () => {
                    this.$api.delete(this.$api.e.asScopeItemDetail, { pk: pk }).then(() => {
                        this.getItems();
                    });
                }
            });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asScopeItemList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        program: {
            handler(value) {
                if (!value) {
                    this.showItemCreateForm = false;
                    this.showScopeCreateForm = false;
                    this.items = [];
                    this.totalRecords = 0;
                    this.filters.scope.value = null;
                }
            }
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #pre-content>
            <PageHeader>Attack Surface Scope</PageHeader>
            <div class="grid grid-cols-3 gap-3">
                <div class="md:col-span-1 col-span-3">
                    <div class="flex items-stretch gap-2 w-full">
                        <div class="flex-1">
                            <ModelCombobox label="Select a program" align="start" :trigger-fluid="true" :fluid="true" variant="form" v-model="program" :api-endpoint="this.$api.e.asProgramList"> </ModelCombobox>
                        </div>
                        <div class="flex-shrink-0">
                            <Button
                                :disabled="!program"
                                @click="
                                    () => {
                                        this.showItemCreateForm = false;
                                        this.showScopeCreateForm = true;
                                    }
                                "
                                ><i class="fa fa-plus"></i> Scope
                            </Button>
                        </div>
                    </div>
                </div>
                <div class="md:col-span-2 col-span-3">
                    <div class="flex items-stretch gap-2 w-full">
                        <div class="flex-1">
                            <SearchField v-model="filters.search.value" @search="onSearch" :disabled="!filters.scope.value"></SearchField>
                        </div>
                        <div class="flex-shrink-0">
                            <Button
                                :disabled="!filters.scope.value"
                                @click="
                                    () => {
                                        this.showScopeCreateForm = false;
                                        this.showItemCreateForm = true;
                                    }
                                "
                                ><i class="fa fa-plus"></i> Item
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <ScopeItemCreateForm class="mb-3" v-model:display="showItemCreateForm" v-model:scope="filters.scope.value" v-if="showItemCreateForm === true" @save="getItems"></ScopeItemCreateForm>
        <ScopeCreateForm v-model:program="program" v-model:display="showScopeCreateForm" v-if="showScopeCreateForm === true" class="mb-3" @save="reloadSidebar = true"></ScopeCreateForm>

        <div class="grid grid-cols-3 gap-3">
            <div class="md:col-span-1 sm:col-span-3">
                <ScopeListSidebar v-model:shouldReload="reloadSidebar" @sidebar-changed="sidebarChanged" v-model:program="program"></ScopeListSidebar>
            </div>
            <div class="sm:col-span-3 md:col-span-2">
                <DataViewContent :items="items" :loading="loading" class="rounded-lg" blank-slate-icon="fa fa-compass" blank-slate-title="No Scope Item!" blank-slate-text="No scope item found!">
                    <template #item="{ item }">
                        <div class="flex">
                            <span v-if="item.results_in === 'Include'">
                                <i class="fa fa-check"></i>
                            </span>
                            <span v-else>
                                <i class="fa fa-warning"></i>
                            </span>
                        </div>

                        <div class="flex-1">
                            <span v-if="item.is_regex === true">[REGEX]: </span>{{ item.value }}
                            <div class="flex">
                                <div class="text-xs text-muted-foreground mt-2">
                                    <span> Created: {{ item.date_created }} </span>
                                    <span class="mx-2">|</span>
                                    <span> Updated: {{ item.date_updated }} </span>
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            {{ item.category }}
                        </div>
                        <div class="flex">
                            <Button variant="destructive" @click="scopeItemDelete(item.pk)"
                                ><i class="fa fa-trash"></i>
                                Delete
                            </Button>
                        </div>
                    </template>
                </DataViewContent>
                <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
            </div>
        </div>
    </ContainerLayout>
</template>
