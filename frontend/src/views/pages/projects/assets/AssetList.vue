<script>
import { BlankSlate } from '@/components/blankslate';
import { AssetBulkEditDialog } from '@/partials/projects';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Button } from '@/components/ui/button';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'AssetList',
    mixins: [listViewMixin],
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            filters: {
                search: { value: null }
            },
            selectedItems: [],
            deleteButtonLoading: false
        };
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pAssetList, { pPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getAssetLink(pk) {
            return this.$router.resolve({
                name: 'AssetDetail',
                params: {
                    projectId: this.projectId,
                    assetId: pk
                }
            }).href;
        }
    },
    mounted() {
        this.getItems();
    },
    components: {
        Paginator,
        DataViewContent,
        Button,
        DataViewHeader,
        SearchField,
        DataViewListLayout,
        AssetBulkEditDialog,
        BlankSlate
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button :href="this.$router.resolve({ name: 'AssetCreate', params: { projectId: this.projectId } }).href"
                as="a"><i class="fa fa-plus"></i> Asset </Button>
        </template>

        <DataViewHeader :total-records="totalRecords"></DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-earth-europe"
            blank-slate-text="No assets found!" blank-slate-title="No Assets!">
            <template #item="{ item }">
                <div class="flex-1">
                    <a :href="this.getAssetLink(item.pk)" class="hover:underline">{{ item.name }}</a>

                    <div class="flex text-sm text-muted-foreground">
                        {{ item.asset_type.name }}
                    </div>
                    <div class="flex text-xs text-muted-foreground">
                        <span>Created: {{ item.date_created }}</span>
                        <span class="mx-2">|</span>
                        <span>Updated: {{ item.date_updated }}</span>
                    </div>
                </div>
                <span>Environment: {{ item.environment }}</span>
                <span>Accessibility: {{ item.accessible }}</span>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
