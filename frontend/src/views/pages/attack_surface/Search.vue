<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import CountryFlag from '@/components/icons/CountryFlag.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import TagBadgeButton from '@/components/badges/TagBadgeButton.vue';
import forceFileDownload from '@/utils/file';

export default {
    name: 'Search',
    components: { TagBadgeButton, BlankSlate, CountryFlag, BaseLayout },
    data() {
        return {
            service: new ASMonitorService(),
            items: [],
            listComposable: useListViewComposable(),
            loading: false,
            filters: {
                protocol: { value: null },
                country: { value: null }
            },
            totalRecords: 0,
            downloadLoading: false,
            searchQuery: null,
            pagination: { page: 1, limit: 20 },
            breadcrumbs: [
                {
                    label: 'Search',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getItems();
    },
    created() {
        const urlParams = new URLSearchParams(window.location.search);
        let searchParam = urlParams.get('search');
        if (searchParam) {
            try {
                this.searchQuery = atob(searchParam);
            } catch (error) {
                this.searchQuery = null;
            }
        }
    },
    methods: {
        onSearch() {
            const encodedSearchQuery = encodeURIComponent(btoa(this.searchQuery));
            this.pagination.page = 1;
            // update the URL without reloading the page
            const newURL = `${window.location.pathname}?search=${encodedSearchQuery}`;
            window.history.pushState({}, '', newURL);

            this.getItems();
        },
        setSearchQuery(value) {
            this.searchQuery = value;
            this.onSearch();
        },
        downloadResults() {
            let downloadLoading = true;
            let params = { download: true };
            if (this.searchQuery) {
                params['search'] = btoa(this.searchQuery);
            }
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.service
                .searchServices(data)
                .then((response) => {
                    forceFileDownload(response);
                })
                .finally(() => {
                    downloadLoading = false;
                });
        },
        getItems(params) {
            this.loading = true;
            if (!params) {
                params = {};
            }
            if (this.searchQuery) {
                params['search'] = btoa(this.searchQuery);
            }
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.service
                .searchServices(data)
                .then((resp) => {
                    this.totalRecords = resp.data.count;
                    this.items = resp.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-span-12 md:col-span-8 md:col-start-3">
            <!-- Search Section -->
            <section>
                <!-- Search Bar -->
                <div class="flex items-center justify-center">
                    <IconField class="w-full">
                        <InputText icon="fa fa-search" v-model="searchQuery" placeholder="Search database" class="w-full" v-on:keyup.enter="onSearch"></InputText>
                        <InputIcon class="fa fa-search"></InputIcon>
                    </IconField>
                </div>
                <!-- End search bar -->
                <div class="flex mt-3">
                    <p class="flex justify-start grow"><span class="font-space-small">Search Results: </span> {{ totalRecords }}</p>
                    <Button @click="downloadResults" size="small" icon="fa fa-download" :loading="downloadLoading"></Button>
                </div>
                <!--
                <div class="mt-6 flex justify-center space-x-4">
                    <Select v-model="filters.protocol.value" :options="serviceProtocolChoices()" optionLabel="label" optionValue="value" placeholder="Protocol" :showClear="true" @change="getItems"></Select>
                    <Select v-model="filters.country.value" :options="[]" placeholder="Country"></Select>
                </div> -->
            </section>

            <!-- Results Section -->
            <div class="pb-3" v-if="loading === false">
                <div v-if="items.length > 0">
                    <Card v-for="item in items" :key="item.pk" class="my-3">
                        <template #header>
                            <div class="flex justify-between items-center border-gray-700 border-b p-4">
                                <h2 class="text-lg font-bold">{{ item.target.data }}</h2>
                                <span class="text-lg">{{ item.protocol.toLowerCase() }}/{{ item.port_number }}/{{ item.service_name }}</span>
                            </div>
                        </template>
                        <template #content>
                            <div class="grid grid-cols-1 gap-6">
                                <div class="flex flex-col md:flex-row">
                                    <div class="md:w-1/3 w-full space-y-3">
                                        <p class="text-blue-500 hover:underline" @click="setSearchQuery(`target.resolved_ip=&quot;${item.target.resolved_ip}&quot;`)">
                                            {{ item.target.resolved_ip || '-' }}
                                        </p>
                                        <p v-if="item.target.asn">
                                            <CountryFlag v-if="item.target.asn.country_code" :country-code="item.target.asn.country_code"></CountryFlag>
                                            {{ item.target.asn.country }} / {{ item.target.asn.region_name }}
                                            /
                                            {{ item.target.asn.city }}
                                        </p>
                                        <p v-if="item.target.asn"><span class="font-bold">ASN:</span> {{ item.target.asn.value }}</p>
                                        <p v-if="item.target.asn && item.target.asn.organisation"><span class="font-bold">Organization:</span> {{ item.target.asn.organisation }}</p>
                                        <p v-if="item.target.asn && item.target.asn.isp"><span class="font-bold">ISP:</span> {{ item.target.asn.isp }}</p>

                                        <p>
                                            <span class="font-bold">Program:</span> <span class="text-blue-500 hover:underline" @click="setSearchQuery(`target.program.id=${item.target.program.pk}`)">{{ item.target.program.name }}</span>
                                        </p>
                                        <p><span class="font-bold">Scope: </span> {{ item.target.scope }}</p>
                                        <p>
                                            <small>Updated: {{ item.target.date_asn_last_updated || 'Never' }}</small>
                                        </p>

                                        <div class="flex flex-wrap gap-2">
                                            <span
                                                class="bg-surface-950 text-white text-sm px-2 py-1 rounded border border-gray-800 hover:bg-surface-800 hover:cursor-pointer"
                                                v-for="technology in item.technologies"
                                                :key="technology.pk"
                                                @click="setSearchQuery(`technologies.name=&quot;${technology.name}&quot;`)"
                                            >
                                                {{ technology.name }}
                                            </span>
                                        </div>

                                        <div class="flex space-x-4">
                                            <router-link :to="{ name: 'AttackSurfaceTargetDetail', params: { targetId: item.target.pk } }" class="text-blue-500 hover:underline" target="_blank">Target Details </router-link>
                                            <a target="_blank" :href="item.scheme" class="text-blue-500 hover:underline" v-if="item.scheme.startsWith('https://') || item.scheme.startsWith('http://')">Visit site</a>
                                        </div>
                                    </div>
                                    <div class="md:w-2/3 w-full md:relative overflow-y-scroll">
                                        <Tabs value="0" class="md:absolute w-full h-full">
                                            <TabList>
                                                <Tab value="0">Banner</Tab>
                                                <Tab value="5" v-if="item.target.description">Description</Tab>
                                                <Tab value="10">Tags</Tab>
                                            </TabList>
                                            <TabPanels class="!bg-surface-950 rounded h-full overflow-y-scroll !max-h-full">
                                                <TabPanel value="0">
                                                    <p class="m-0 whitespace-pre">{{ item.banner || 'Not enough data' }}</p>
                                                </TabPanel>
                                                <TabPanel value="5">
                                                    <p class="m-0 whitespace-pre">{{ item.target.description }}</p>
                                                </TabPanel>
                                                <TabPanel value="10">
                                                    <p v-if="item.tags.length > 0">
                                                        <TagBadgeButton :key="tag.pk" :label="tag" v-for="tag in item.tags"></TagBadgeButton>
                                                    </p>
                                                    <p v-else>-</p>
                                                </TabPanel>
                                            </TabPanels>
                                        </Tabs>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>
                </div>
                <div class="card" v-else>
                    <BlankSlate title="No Results!" text="No Results found for your query" icon="fa fa-face-sad-tear"></BlankSlate>
                </div>
            </div>
            <!-- loading skeleton -->
            <div class="py-3" v-else>
                <Card>
                    <template #content>
                        <Skeleton class="mb-2"></Skeleton>
                        <Skeleton width="10rem" class="mb-2"></Skeleton>
                        <Skeleton width="5rem" class="mb-2"></Skeleton>
                        <Skeleton height="2rem" class="mb-2"></Skeleton>
                        <Skeleton width="10rem" height="4rem"></Skeleton>
                    </template>
                </Card>
            </div>
            <div class="pb-6">
                <Paginator :total-records="this.totalRecords" :rows="this.pagination.limit" @page="onPage"></Paginator>
            </div>
        </div>
    </BaseLayout>
</template>
