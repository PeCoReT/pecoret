<script>
import { useAuthStore } from '@/store/auth';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import { Card } from '@/components/card';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import { Button } from '@/components/ui/button';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import RadioDropdownMenu from '@/components/dropdown-menu/RadioDropdownMenu.vue';
import { Paginator } from '@/components/paginator';
import { Select } from '@/components/select';
import { listViewMixin } from "@/mixins/listViewMixin";

export default {
    name: 'ProjectList',
    mounted() {
        this.authStore.deactivateProject();
        this.getProjects();
        this.getPinnedProjects();
    },
    mixins: [listViewMixin],
    data() {
        return {
            authStore: useAuthStore(),
            projects: [],
            pinnedProjects: [],
            loading: false,
            selection: {},
            deleteButtonLoading: false,
            sortItems: commonSortFilter,
            filters: {
                search: { value: null },
                status: { value: 'Open' },
                ordering: { value: '-date_created' }
            },
            statusChoices: [
                {
                    label: 'Open',
                    value: 'Open'
                },
                {
                    label: 'Closed',
                    value: 'Closed'
                }
            ]
        };
    },
    methods: {
        onGlobalSearch(query) {
            this.getProjects({ search: query });
        },
        getPinnedProjects() {
            let params = {
                pinned: true
            };
            this.$api.get(this.$api.e.projectList, null, params).then((response) => {
                this.pinnedProjects = response.data.results;
            });
        },
        getProjects(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.projectList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.projects = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        async bulkPatch(data) {
            for (const [key, value] of Object.entries(this.selection)) {
                if (value === true) {
                    await this.$api.patch(this.$api.e.projectDetail, { pk: key }, data);
                }
            }
            this.selection = {};
            this.getProjects();
        },
        async bulkDelete() {
            this.$confirm.require({
                accept: async () => {
                    let itemsDeleted = 0;
                    let totalLength = Object.entries(this.selection).length;
                    for (const [key, value] of Object.entries(this.selection)) {
                        itemsDeleted++;
                        if (value === true) {
                            await this.$api
                                .delete(this.$api.e.projectDetail, {
                                    pk: key
                                })
                                .then(() => {
                                    if (itemsDeleted === totalLength) {
                                        this.selection = {};
                                        this.getProjects();
                                    }
                                });
                        }
                    }
                }
            });
        },
        onPage(page) {
            this.pagination.page = page;
            this.getProjects();
        }
    },
    components: {
        Select,
        Paginator,
        RadioDropdownMenu,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout,
        BaseListLayout,
        Card,
        Button
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onGlobalSearch"></SearchField>
        </template>
        <template #create-button>
            <Button>
                <a :href="this.$router.resolve({ name: 'ProjectCreate' }).href"> <i class="fa fa-plus"></i> Project </a>
            </Button>
        </template>

        <div v-if="pinnedProjects.length > 0" class="mb-3 mt-3 grid sm:grid-cols-2 md:grid-cols-6 gap-4">
            <div v-for="project in pinnedProjects" v-bind:key="project.pk" class="">
                <Card class="pb-3 px-2">
                    <router-link :to="{ name: 'ProjectDetail', params: { projectId: project.pk } }"
                        class="text-color underline">
                        {{ project.name }}
                    </router-link>
                    <br />
                    <small>{{ project.status }} / {{ project.company.name }}</small>
                </Card>
            </div>
        </div>

        <DataViewHeader :total-records="totalRecords" v-model:items="projects" v-model:selection="selection"
            :show-bulk-select="true">
            <template #filters>
                <RadioDropdownMenu v-model="filters.status.value" :items="statusChoices" label="Status"
                    @select="getProjects()"></RadioDropdownMenu>
                <SortListDropdownMenu :items="sortItems" v-model="filters.ordering.value"
                    @update:model-value="getProjects()"></SortListDropdownMenu>
            </template>
            <template #bulk>
                <Select :options="statusChoices" placeholder="Status" @update:model-value="
                    (value) => {
                        bulkPatch({ status: value });
                    }
                "></Select>
                <Button @click="bulkDelete" variant="destructive">Delete</Button>
            </template>
        </DataViewHeader>

        <DataViewContent :show-bulk-select="true" v-model:selection="selection" :items="projects" :loading="loading"
            blank-slate-icon="fa fa-box" blank-slate-text="No projects found!" blank-slate-title="No Projects!">
            <template #item="{ item }">
                <div>
                    <i v-if="item.status === 'Open'" class="fa fa-lock-open"></i>
                    <i v-else class="fa fa-lock"></i>
                </div>

                <div class="flex-1">
                    <div class="flex justify-between items-center">
                        <div class="font-bold">
                            <a :href="this.$router.resolve({ name: 'ProjectDetail', params: { projectId: item.pk } }).href"
                                class="font-normal hover:underline"> [{{ item.year }}] {{ item.name }} </a>
                        </div>
                        {{ item.company.name }}
                    </div>

                    <div class="flex flex-wrap">
                        <span v-for="tag in item.tags" :key="tag.pk"
                            class="bg-background text-accent-foreground text-sm px-2 py-1 rounded border border-gray-800 hover:bg-surface-800 hover:cursor-pointer">
                            {{ tag.name }}
                        </span>
                    </div>

                    <div class="text-xs text-gray-500 mt-2">
                        <span> ID: {{ item.pk }} </span>
                        <span class="mx-2">|</span>
                        <span>
                            Created: <span class="font-medium">{{ item.date_created }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span>
                            Updated: <span class="font-medium">{{ item.date_updated }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span>
                            {{ item.visibility }}
                        </span>
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
