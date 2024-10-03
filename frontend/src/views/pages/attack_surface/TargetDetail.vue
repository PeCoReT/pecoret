<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import ASMonitorService from '@/service/ASMonitorService';
import CountryFlag from '@/components/icons/CountryFlag.vue';

export default {
    name: 'TargetDetail',
    components: { CountryFlag, BaseLayout },
    data() {
        return {
            service: new ASMonitorService(),
            targetId: this.$route.params.targetId,
            target: {},
            loading: false,
            breadcrumbs: [
                {
                    label: 'Targets',
                    disabled: true
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
    },
    methods: {
        getItem() {
            this.loading = true;
            this.service
                .getTarget(this.targetId)
                .then((resp) => {
                    this.target = resp.data;
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
                        <th class="text-left">IP Address:</th>
                        <td>{{ target.resolved_ip }}</td>
                    </tr>
                    <tr>
                        <th class="text-left">Country:</th>
                        <td v-if="target.asn">
                            <CountryFlag v-if="target.asn" :country-code="target.asn.country_code"></CountryFlag>
                            {{ target.asn.country }}
                        </td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">City:</th>
                        <td v-if="target.asn">{{ target.asn.city }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">Organization:</th>
                        <td v-if="target.asn">{{ target.asn.organization || '-' }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">ISP:</th>
                        <td v-if="target.asn">{{ target.asn.isp }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">ASN:</th>
                        <td v-if="target.asn">{{ target.asn.value }}</td>
                        <td v-else>-</td>
                    </tr>
                    <tr>
                        <th class="text-left">Last Updated:</th>
                        <td>{{ target.date_updated }}</td>
                    </tr>
                    <tr>
                        <th class="text-left">Hostnames:</th>
                        <td v-if="target.hostnames && target.hostnames.length > 0">
                            <span v-for="hostname in target.hostnames" :key="hostname" class="inline-flex items-center rounded-md bg-slate-800 px-2 py-1 font-medium text-gray-300 ring-1 ring-inset ring-gray-50/10 mt-3 mr-2">
                                {{ hostname }}
                            </span>
                        </td>
                        <td v-else>-</td>
                    </tr>
                </table>
            </div>
        </div>
    </BaseLayout>
</template>
