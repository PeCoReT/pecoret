<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import CountryFlag from '@/components/icons/CountryFlag.vue';
import { BlankSlate } from '@/components/blankslate';
import forceFileDownload from '@/utils/file';
import { ModalDialog } from '@/components/dialog';
import { Badge } from '@/components/badge';
import { Card } from '@/components/card';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { AttackSurfaceSaveQueryDialog } from '@/partials/attack_surface';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import SearchField from '@/partials/common/SearchField.vue';
import { Input } from '@/components/ui/input';
import { MagnifyingGlassIcon } from '@radix-icons/vue';
import { Button } from '@/components/ui/button';
import { Paginator } from '@/components/paginator';
import { commonSortFilter } from '@/utils/constants';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { listViewMixin } from '@/mixins/listViewMixin';
import TechnologyBadge from "@/partials/knowledgebase/TechnologyBadge.vue";

export default {
    name: 'Search',
    mixins: [listViewMixin],
    components: {
        TechnologyBadge,
        SortListDropdownMenu,
        Paginator,
        Button,
        MagnifyingGlassIcon,
        Input,
        SearchField,
        ModelCombobox,
        DefaultSkeleton,
        AttackSurfaceSaveQueryDialog,
        Badge,
        ModalDialog,
        BlankSlate,
        CountryFlag,
        BaseLayout,
        Card
    },
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                ordering: { value: '-date_created' }
            },
            saveQueryModal: false,
            downloadLoading: false,
            searchQuery: null,
            searchQueries: [],
            activeSearchQuery: null,
            sortItems: commonSortFilter
        };
    },
    mounted() {
        this.getItems();
    },
    created() {
        if (this.$route.query.search) {
            try {
                this.searchQuery = atob(decodeURIComponent(this.$route.query.search));
            } catch (error) {
                console.log(error);
                this.searchQuery = null;
            }
        }
    },
    methods: {
        onSearch() {
            const encodedSearchQuery = encodeURIComponent(btoa(this.searchQuery));
            this.pagination.page = 1;

            const currentQueryParams = { ...this.$route.query };
            const newParams = { ...currentQueryParams, search: encodedSearchQuery };
            this.$router.push({ query: newParams });

            this.getItems();
        },
        setSearchQuery(value) {
            this.searchQuery = value;
            this.onSearch();
        },
        downloadResults() {
            this.downloadLoading = true;
            let params = { download: true };
            if (this.searchQuery) {
                params['ql'] = btoa(this.searchQuery);
            }
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asServiceSearch, null, data)
                .then((response) => {
                    forceFileDownload(response);
                })
                .finally(() => {
                    this.downloadLoading = false;
                });
        },
        getItems(params) {
            this.loading = true;
            if (!params) {
                params = {};
            }
            if (this.searchQuery) {
                params['ql'] = btoa(this.searchQuery);
            }
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asServiceSearch, null, data)
                .then((resp) => {
                    this.totalRecords = resp.data.count;
                    this.items = resp.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        setActiveQuery(value) {
            this.searchQuery = value.query;
        },
        confirmQueryDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this query?',
                accept: () => {
                    this.$api.delete(this.$api.e.asSearchQueryDetail, { pk: this.activeSearchQuery }).then(() => {
                        this.$toaster({
                            title: 'Confirmed',
                            description: 'Query deleted!',
                            duration: 3000
                        });
                    });
                    this.activeSearchQuery = null;
                    this.searchQuery = null;
                }
            });
        }
    }
};
</script>

<template>
    <BaseLayout>
        <div class="md:col-span-12 lg:col-span-8 lg:col-start-3">
            <!-- Search Section -->
            <section>
                <!-- Search Bar -->
                <div class="flex items-center justify-start space-x-2">
                    <!-- Combobox trigger button -->
                    <ModelCombobox v-model="activeSearchQuery" :api-endpoint="this.$api.e.asSearchQueryList" align="start" label="Queries" @select="setActiveQuery" :fluid="true">
                        <template #trigger>
                            <Button variant="outline">Queries <i class="fa fa-chevron-down"></i></Button>
                        </template>
                    </ModelCombobox>

                    <!-- Search field -->
                    <div class="relative w-full items-center">
                        <Input id="search" v-model="searchQuery" class="pr-10" placeholder="Search QL" type="text" v-on:keyup.enter="onSearch"></Input>
                        <span class="absolute end-0 inset-y-0 flex items-center justify-center px-2">
                            <MagnifyingGlassIcon class="size-6 text-muted-foreground" @click="onSearch" />
                        </span>
                    </div>

                    <AttackSurfaceSaveQueryDialog :query="searchQuery"></AttackSurfaceSaveQueryDialog>

                    <Button :disabled="!activeSearchQuery" variant="destructive" @click="confirmQueryDelete"><i class="fa fa-trash"></i> Delete </Button>
                </div>

                <!-- End search bar -->
                <div class="flex items-center my-3">
                    <p class="flex justify-start grow"><span class="font-space-small">Search Results: </span> {{ totalRecords }}</p>
                    <SortListDropdownMenu v-model="filters.ordering.value" :items="sortItems" @update:model-value="getItems()"></SortListDropdownMenu>
                    <Button :loading="downloadLoading" variant="secondary" @click="downloadResults"><i class="fa fa-download" /> Download </Button>
                </div>
            </section>

            <!-- Results Section -->
            <div v-if="loading === false" class="pb-3">
                <div v-if="items.length > 0">
                    <Card v-for="item in items" :key="item.pk" class="my-3 py-2">
                        <template #title>
                            <div class="flex justify-between items-center border-input border-b">
                                <h2 class="font-bold text-lg">{{ item.target.data }}</h2>
                                <span class="text-lg">{{ item.protocol.toLowerCase() }}/{{ item.port_number }}/{{ item.service_name }}</span>
                            </div>
                        </template>
                        <div class="grid grid-cols-1 gap-6">
                            <div class="flex flex-col md:flex-row">
                                <div class="md:w-1/3 w-full space-y-2">
                                    <p class="text-muted-foreground hover:underline hover:cursor-pointer" @click="setSearchQuery(`target.resolved_ip=&quot;${item.target.resolved_ip}&quot;`)">
                                        {{ item.target.resolved_ip || '-' }}
                                    </p>
                                    <p v-if="item.target.asn" class="flex">
                                        <CountryFlag v-if="item.target.asn.country_code" :country-code="item.target.asn.country_code"></CountryFlag>
                                        {{ item.target.asn.country }} / {{ item.target.asn.region_name }}
                                        /
                                        {{ item.target.asn.city }}
                                    </p>
                                    <p v-if="item.target.asn"><span class="font-bold">ASN:</span> {{ item.target.asn.value }}</p>
                                    <p v-if="item.target.asn && item.target.asn.organisation"><span class="font-bold">Organization:</span> {{ item.target.asn.organisation }}</p>
                                    <p v-if="item.target.asn && item.target.asn.isp"><span class="font-bold">ISP:</span> {{ item.target.asn.isp }}</p>

                                    <p>
                                        <span class="font-bold">Program: </span>
                                        <span class="text-muted-foreground hover:underline hover:cursor-pointer" @click="setSearchQuery(`target.program.id=${item.target.program.pk}`)"> {{ item.target.program.name }}</span>
                                    </p>
                                    <p><span class="font-bold">Scope: </span> {{ item.target.scope }}</p>
                                    <p>
                                        <small>Created: {{ item.date_created }}</small>
                                        <small class="mx-2">|</small>
                                        <small>Updated: {{ item.date_updated }}</small>
                                    </p>
                                    <div class="flex flex-wrap gap-2" v-if="item.tags.length > 0">
                                        <Badge v-for="tag in item.tags" :key="tag.pk" :color="tag.color" :text="tag.name" class="hover:cursor-pointer" @click="setSearchQuery(`tags.name=&quot;${tag.name}&quot;`)"></Badge>
                                    </div>

                                    <div class="flex space-x-4">
                                        <router-link :to="{ name: 'AttackSurfaceTargetDetail', params: { targetId: item.target.pk } }" class="text-muted-foreground hover:underline" target="_blank">Target Details </router-link>
                                        <a v-if="item.scheme.startsWith('https://') || item.scheme.startsWith('http://')" :href="item.scheme" class="text-muted-foreground hover:underline" target="_blank">Visit site</a>
                                    </div>
                                </div>
                                <div class="md:w-2/3 w-full md:relative overflow-y-scroll">
                                    <div class="w-full h-full md:absolute">
                                        <div class="border rounded-xl h-full overflow-y-scroll max-h-full bg-muted py-2 px-3">
                                            <p class="m-0 whitespace-pre p-2">
                                                {{ item.banner || 'Not enough data' }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="flex flex-wrap gap-2">
                                <TechnologyBadge :technology="technology" :key="technology.pk" v-for="technology in item.technologies"
                                     @click="setSearchQuery(`technologies.name=&quot;${technology.name}&quot;`)"
                                ></TechnologyBadge>
                            </div>
                        </div>
                    </Card>
                </div>
                <div v-else class="card">
                    <BlankSlate icon="fa fa-face-sad-tear" text="No Results found for your query" title="No Results!"></BlankSlate>
                </div>
            </div>
            <!-- loading skeleton -->
            <div v-else class="py-3">
                <Card>
                    <DefaultSkeleton></DefaultSkeleton>
                </Card>
            </div>
            <div class="pb-6">
                <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
            </div>
        </div>
    </BaseLayout>
</template>
