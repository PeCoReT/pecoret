<script>
import { BlankSlate } from '@/components/blankslate';
import { CommandUpdate, ProjectCommandCreate } from '@/partials/projects';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'CommandList',
    mounted() {
        this.getItems();
    },
    mixins: [listViewMixin],
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            selectedItems: [],
            deleteButtonLoading: false,
            loading: false,
            filters: {}
        };
    },
    methods: {
        commonSortFilter() {
            return commonSortFilter;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pCommandList, { projectPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        Paginator,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        DataViewListLayout,
        CommandUpdate,
        BlankSlate,
        ProjectCommandCreate
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #create-button>
            <ProjectCommandCreate @object-created="getItems"></ProjectCommandCreate>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-terminal" blank-slate-text="No commands found!" blank-slate-title="No Commands!">
            <template #item="{ item }">
                <div class="flex-1">
                    {{ item.command }}
                    <div class="flex text-xs text-muted-foreground">run on {{ item.date_run }} by {{ item.user.username }}</div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
