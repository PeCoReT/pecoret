<script>
import CountryFlag from '@/components/icons/CountryFlag.vue';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';

export default {
    name: 'TargetDetail',
    components: { DataViewListLayout, CountryFlag},
    data() {
        return {
            targetId: this.$route.params.targetId,
            target: {},
            loading: false
        };
    },
    mounted() {
        this.getItem();
    },
    methods: {
        getItem() {
            this.loading = true;
            this.$api
                .get(this.$api.e.asTargetDetail, { pk: this.targetId })
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
    <DataViewListLayout>
        <Card class="bg-background mb-3">
            <h2 class="text-3xl font-bold mb-3">Target Detail</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <p><strong>Data:</strong></p>
                    <p>{{ target.data }}</p>
                    <p><strong>Resolved IP:</strong></p>
                    <p>{{ target.resolved_ip || '-' }}</p>
                    <p><strong>Scope:</strong></p>
                    <p>{{ target.scope }}</p>
                    <p><strong>Data Type:</strong></p>
                    <p>
                        <span class="badge badge-important">{{ target.data_type }}</span>
                    </p>
                </div>
                <div>
                    <p><strong>Program:</strong></p>
                    <p>
                        <span v-if="target.program">{{ target.program.name }}</span> <span v-else>-</span>
                    </p>
                    <p><strong>Date Created:</strong></p>
                    <p>{{ target.date_created }}</p>
                    <p><strong>Date Updated:</strong></p>
                    <p>{{ target.date_updated }}</p>
                </div>
            </div>
            <div class="grid grid-cols-1 gap-4 mt-3" v-if="target.description">
                <h3 class="font-bold text-lg">Description:</h3>
                <span>{{ target.description }}</span>
            </div>
        </Card>
        <Card class="bg-background mb-3">
            <h2 class="text-2xl font-bold mb-3">Hostnames</h2>
            <span v-for="hostname in target.hostnames" :key="hostname" class="inline-flex items-center rounded-md bg-slate-800 px-2 py-1 font-medium text-gray-300 ring-1 ring-inset ring-gray-50/10 mt-3 mr-2">
                {{ hostname }}
            </span>
            <span v-if="!target.hostnames || target.hostnames.length < 1">-</span>
        </Card>

        <Card class="bg-background mb-3">
            <h2 class="text-3xl font-bold mb-3">ASN Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <p><strong>Name:</strong></p>
                    <p v-if="target.asn">{{ target.asn.value }} {{ target.asn.name || '-' }}</p>
                    <p v-else>-</p>
                    <p><strong>Address:</strong></p>
                    <p v-if="target.asn">
                        <CountryFlag v-if="target.asn" :country-code="target.asn.country_code"></CountryFlag>
                        {{ target.asn.country }}
                    </p>
                    <p v-else>-</p>
                    <p v-if="target.asn">{{ target.asn.zipcode }} {{ target.asn.city }}, {{ target.asn.region_name }}</p>
                    <p v-else>-</p>
                </div>
                <div>
                    <p><strong>Timezone:</strong></p>
                    <p v-if="target.asn">{{ target.asn.timezone || '-' }}</p><p v-else>-</p>
                    <p><strong>ISP / Organization:</strong></p>
                    <p v-if="target.asn">{{ target.asn.isp || '-' }} / {{ target.asn.organization || '-' }}</p><p v-else>-</p>
                </div>
            </div>
            <p><strong>Date ASN Last Updated:</strong></p>
            <p>{{ target.date_asn_last_updated || '-' }}</p>
        </Card>
    </DataViewListLayout>
</template>
