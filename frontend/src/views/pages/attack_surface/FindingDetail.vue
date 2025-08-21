<script>
import { useAuthStore } from '@/store/auth';
import { MarkdownEditor } from '@/components/editor';
import forceFileDownload from '@/utils/file';
import { AffectedComponentFindingCard } from '@/partials/attack_surface';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/select';
import { DetailCardWithIcon } from '@/components/card';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { ReloadIcon } from '@radix-icons/vue';

export default {
    name: 'FindingDetail',
    components: {
        ReloadIcon,
        DetailCardWithIcon,
        ContainerLayout,
        DefaultSkeleton,
        MultiModelCombobox,
        AffectedComponentFindingCard,
        MarkdownEditor,
        Input,
        Button,
        Select
    },
    data() {
        return {
            model: {},
            authStore: useAuthStore(),
            findingId: this.$route.params.findingId,
            loaded: false,
            downloadLoading: false
        };
    },
    mounted() {
        this.getItem();
    },
    computed: {
        editButtonDisabled() {
            return this.model.is_locked === true && this.model.locked_by.pk !== this.authStore.me.pk;
        }
    },
    methods: {
        getItem() {
            this.$api.get(this.$api.e.asFindingDetail, { pk: this.findingId }).then((response) => {
                this.model = response.data;
                this.loaded = true;
            });
        },
        downloadPDF() {
            this.downloadLoading = true;
            this.$api
                .get(this.$api.e.asFindingPdf, { pk: this.findingId }, null, { responseType: 'arraybuffer' })
                .then((response) => {
                    forceFileDownload(response);
                })
                .finally(() => {
                    this.downloadLoading = false;
                });
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this finding?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.asFindingDetail, { pk: this.findingId });
                    this.$router.push({ name: 'AttackSurfaceFindingList' });
                }
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <h2 class="text-2xl font-semibold truncate">{{ model.title }}</h2>
        </template>
        <template #right-header>
            <Button :disabled="downloadLoading" class="mr-2 mb-2 sm:mb-0" @click="downloadPDF">
                <ReloadIcon class="animate-spin" v-if="downloadLoading" />
                <i class="fa fa-download" v-else />
                Download
            </Button>
            <Button :disabled="editButtonDisabled" class="mr-2 mb-2 sm:mb-0" as="a" variant="outline" :href="this.$router.resolve({ name: 'AttackSurfaceFindingUpdate', params: { pk: this.findingId } }).href">
                <i class="fa fa-edit" />
                Edit
                <span v-if="model.is_locked">
                    <small class="ml-1">(Locked by {{ model.locked_by.username }})</small>
                </span>
            </Button>
            <Button variant="destructive" :disabled="model.locked_by" @click="confirmDialogDelete"> <i class="fa fa-trash"></i> Delete </Button>
        </template>

        <div v-if="loaded" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <DetailCardWithIcon :text="model.severity" icon="fa fa-shield-halved" title="Severity" />
            <DetailCardWithIcon :text="model.status" icon="fa fa-bookmark" title="Status" />
        </div>

        <div v-if="loaded" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <h4 class="text-md font-bold">CVSS-Score</h4>
                    <div>{{ model.cvss_score }}</div>
                </div>
                <div>
                    <h4 class="text-md font-bold">CWEs</h4>
                    <ul class="list-disc list-inside">
                        <li v-for="cwe in model.cwe_ids" :key="cwe.id">{{ cwe.display_name }} ({{ cwe.name }})</li>
                    </ul>
                </div>
            </div>

            <div>
                <h4 class="text-md font-bold">Description</h4>
                <div class="markdown-block" v-html="model.description_html"></div>
            </div>

            <div>
                <h4 class="text-md font-bold">Exploitation Details</h4>
                <div class="markdown-block" v-html="model.exploitation_details_html"></div>
            </div>

            <div>
                <h4 class="text-md font-bold">Recommendation</h4>
                <div class="markdown-block" v-html="model.recommendation_html"></div>
            </div>

            <hr />

            <div>
                <h4 class="text-md font-bold">Internal Notes</h4>
                <div class="markdown-block" v-html="model.internal_notes_html"></div>
            </div>
        </div>

        <div v-else class="grid w-full">
            <DefaultSkeleton />
        </div>

        <AffectedComponentFindingCard v-if="loaded" />
    </ContainerLayout>
</template>
