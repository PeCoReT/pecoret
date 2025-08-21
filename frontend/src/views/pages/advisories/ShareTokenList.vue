<script>
import { AdvisoryTabMenu, ShareTokenCreateDialog } from '@/partials/advisories';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Badge } from '@/components/badge';
import { Button } from '@/components/ui/button';
import { commonSortFilter } from '@/utils/constants';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import {listViewMixin} from "@/mixins/listViewMixin";

export default {
    name: 'ShareTokenList',
    mixins: [listViewMixin],
    components: {
        ContainerLayout,
        Badge,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        ShareTokenCreateDialog,
        AdvisoryTabMenu,
        Button
    },
    data() {
        return {
            loading: false,
            items: [],
            advisoryId: this.$route.params.advisoryId,
            sortItems: commonSortFilter
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        copyToClipboard(data) {
            navigator.clipboard.writeText(data);
            this.$toaster({
                title: 'Copied',
                description: 'URL copied to clipboard!',
                duration: 3000
            });
        },
        getItems(params) {
            this.loading = true;
            params = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.aShareTokenList, { aPk: this.advisoryId }, params)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this token?',
                accept: () => {
                    this.$api.delete(this.$api.e.aShareTokenDetail, { aPk: this.advisoryId, pk: id }).then(() => {
                        this.$toaster({
                            title: 'Deleted',
                            description: 'Token was removed!',
                            duration: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <AdvisoryTabMenu></AdvisoryTabMenu>
        </template>
        <template #right-header>
            <ShareTokenCreateDialog @object-created="getItems"></ShareTokenCreateDialog>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <SortListDropdownMenu :items="sortItems" @sort="sort"></SortListDropdownMenu>
            </template>
        </DataViewHeader>

        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-share" blank-slate-text="No share tokens found!" blank-slate-title="No Share Tokens!">
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex justify-between items-center">
                        {{ item.name }}
                        <div class="flex items-center space-x-4 text-sm">
                            <Button @click="copyToClipboard(item.url)"><i class="fa fa-copy" /></Button>
                            <Button variant="destructive" @click="confirmDialogDelete(item.pk)"><i class="fa fa-trash"></i> Delete </Button>
                        </div>
                    </div>
                </div>
            </template>
        </DataViewContent>
    </ContainerLayout>
</template>
