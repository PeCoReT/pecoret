<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import ASMonitorService from '@/service/ASMonitorService';
import CountryFlag from '@/components/icons/CountryFlag.vue';
import HostPortTable from '@/components/table/HostPortTable.vue';


export default {
    name: 'HostDetail',
    components: { HostPortTable, CountryFlag, BaseLayout },
    data() {
        return {
            service: new ASMonitorService(),
            hostId: this.$route.params.hostId,
            host: {},
            loading: false,
            breadcrumbs: [
                {
                    label: 'Hosts',
                    disabled: true
                },
                {
                    label: 'Host Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getItem();
    },
    methods: {
        getItem() {
            this.loading = true;
            this.service
                .getHost(this.hostId)
                .then((resp) => {
                    this.host = resp.data;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-span-12">
            <div class="card">
                <table class="table-auto w-full">
                    <tr>
                        <th class="text-left">Country:</th>
                        <td v-if="host.asn">
                            <CountryFlag v-if="host.asn" :country-code="host.asn.country_code"></CountryFlag>
                            {{ host.asn.country }}
                        </td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">City:</th>
                        <td v-if="host.asn">{{ host.asn.city }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">Organization:</th>
                        <td v-if="host.asn">{{ host.asn.organization || '-' }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">ISP:</th>
                        <td v-if="host.asn">{{ host.asn.isp }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">ASN:</th>
                        <td v-if="host.asn">{{ host.asn.value }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">Last Updated:</th>
                        <td>{{ host.date_updated }}</td>
                    </tr>
                    <tr>
                        <th class="text-left">Hostnames:</th>
                        <td v-if="host.hostnames && host.hostnames.length > 0">
                            <span v-for="hostname in host.hostnames" :key="hostname" class="inline-flex items-center rounded-md bg-slate-800 px-2 py-1 font-medium text-gray-300 ring-1 ring-inset ring-gray-50/10 mt-3 mr-2">
                                {{ hostname }}
                            </span>
                        </td>
                        <td v-else>-</td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="col-span-12">
            <div class="card">
                <HostPortTable :host="host"></HostPortTable>
            </div>
        </div>
    </BaseLayout>
</template>
