<script>
export default {
    name: 'AssetTechnologyCards',
    props: {
        technologies: {
            required: true
        }
    },
    watch: {
        technologies: {
            immediate: true,
            deep: true
        }
    }
};
</script>

<template>
    <div class="grid mt-3 grid-cols-1" v-if="technologies && technologies.length > 1">
        <div class="col-span-1">
            <h2 class="text-2xl font-semibold">Assigned Technologies</h2>
            <div class="mt-4 grid gap-6 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-6">
                <div class="bg-surface-950 p-5 rounded-lg shadow-md" v-for="technology in technologies" :key="technology.pk">
                    <h3 class="text-lg font-bold">{{ technology.name }}</h3>
                    <p class="mt-2"><span class="font-semibold">Vendor:</span> {{ technology.vendor_name || '-' }}</p>
                    <p><span class="font-semibold">CPE:</span> {{ technology.cpe }}</p>
                </div>
            </div>
        </div>
    </div>
</template>
