<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { Badge } from '@/components/badge';
import ContainerLayout from "@/layouts/ContainerLayout.vue";
import BlankSlate from "@/components/blankslate/BlankSlate.vue";

export default {
    name: 'ScanFindingDetail',
    components: { BlankSlate, ContainerLayout, BaseLayout, Badge },
    data() {
        return {
            item: {},
            urlId: this.$route.params.urlId,
            breadcrumbs: [
                {
                    label: 'URLs',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceURLList'
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getFinding();
    },
    methods: {
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this url?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.asUrlDetail, { pk: this.urlId }).then(() => {
                        this.$router.push({
                            name: 'AttackSurfaceURLList'
                        });
                    });
                }
            });
        },
        getFinding() {
            this.$api.get(this.$api.e.asUrlDetail, { pk: this.urlId }).then((response) => {
                this.item = response.data;
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <h2 class="text-2xl font-semibold mb-2">URL: {{ item.url }}</h2>
        <p class="mb-2"><strong>Status Code:</strong> {{ item.status_code || 'Unknown' }}</p>
        <p class="mb-2"><strong>Ssdeep Headers:</strong> {{ item.fuzzy_hash_headers || '-' }}</p>
        <p class="mb-2"><strong>Ssdeep Body:</strong> {{ item.fuzzy_hash_body || '-' }}</p>

        <div v-if="item.technologies && item.technologies.length > 0" id="technologies">
            <p class="mb-4"><strong>Technologies:</strong></p>
            <div class="flex flex-wrap space-x-2 mb-4">
                <span v-for="technology in item.technologies" :key="technology.pk"
                    class="bg-accent text-accent-foreground text-sm px-2 py-1 rounded border">{{ technology.name
                    }}</span>
            </div>
        </div>

        <div v-if="item.tags && item.tags.length > 0" id="tags">
            <p class="mb-2"><strong>Tags:</strong></p>
            <Badge v-for="tag in item.tags" :key="tag.pk" :color="tag.color" :text="tag.name"></Badge>
        </div>

        <div v-if="item.response" class="mt-3">
            <h3 class="text-xl font-semibold mb-2">Response</h3>
            <Card class="bg-background">
                <code style="white-space: pre-wrap">{{ item.response.slice(0, 10000) }}</code>
            </Card>
        </div>
        <Card v-else>
            <BlankSlate title="Not enough data" text="No response data found for this URL!" icon="fa fa-exclamation">
            </BlankSlate>
        </Card>
    </ContainerLayout>
</template>
