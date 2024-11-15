<script>
export default {
    name: 'AssetSelectField',
    props: {
        modelValue: {
            required: true
        },
        displayInline: {
            default: false
        },
        hideLabels: {
            default: false
        }
    },
    emits: ['update:modelValue'],
    data() {
        return {
            asset: null,
            assetType: null,
            projectId: this.$route.params.projectId,
            assetChoices: null,
            choices: [
                {
                    label: 'Web Application',
                    value: 'web_application',
                    url: 'web-applications'
                },
                {
                    label: 'Host',
                    value: 'host',
                    url: 'hosts'
                },
                {
                    label: 'Service',
                    value: 'service',
                    url: 'services'
                },
                {
                    label: 'Mobile Application',
                    value: 'mobile_application',
                    url: 'mobile-applications'
                },
                {
                    label: 'Thick Client',
                    value: 'thick_client',
                    url: 'thick-clients'
                },
                {
                    label: 'Generic',
                    value: 'generic_asset',
                    url: 'generic-assets'
                }
            ]
        };
    },
    methods: {
        loadAssets() {
            let url = '/projects/' + this.projectId + '/' + this.assetType.url + '/';
            this.$api.get(url).then((response) => {
                this.assetChoices = response.data.results;
            });
        },
        onFilter(event) {
            let config = {
                params: {
                    search: event.value
                }
            };
            let url = '/projects/' + this.projectId + '/' + this.assetType.url + '/';
            this.$api.get(url, config).then((response) => {
                this.assetChoices = response.data.results;
            });
        }
    },
    computed: {
        assetObject() {
            return { pk: this.asset.pk, type: this.assetType.value };
        },
    }
};
</script>

<template>
    <InlineField v-if="displayInline === true">
        <Select :options="choices" v-model="assetType" placeholder="Asset Type" optionLabel="label" @change="loadAssets"></Select>
    </InlineField>
    <InlineField v-if="displayInline === true">
        <Select :options="assetChoices" v-model="asset" placeholder="Asset" :disabled="!this.assetType" optionLabel="display_name" filter @filter="onFilter" @update:modelValue="this.$emit('update:modelValue', this.assetObject)"></Select>
    </InlineField>

    <Field v-if="displayInline !== true" :label="assetTypeLabel">
        <Select :options="choices" v-model="assetType" id="asset_type" optionLabel="label" @change="loadAssets"></Select>
    </Field>
    <Field v-if="displayInline !== true" label="Asset">
        <Select :options="assetChoices" v-model="asset" id="asset" :disabled="!this.assetType" optionLabel="display_name" filter @filter="onFilter" @update:modelValue="this.$emit('update:modelValue', this.assetObject)"></Select>
    </Field>
</template>