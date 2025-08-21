<script>
export default {
    name: 'BlankSlate',
    props: {
        icon: {
            required: true
        },
        title: {
            required: true
        },
        text: {
            required: true
        }
    }
};
</script>

<template>
    <div class="grid grid-cols-12">
        <div class="col-span-12 text-center">
            <div class="items-center justify-center p-16">
                <p class="mb-3 text-xl">
                    <i :className="this.icon + ' fa-2x'"></i>
                </p>
                <h2 class="text-2xl">{{ this.title }}</h2>
                <p class="text-disabled mt-3">
                    {{ this.text }}
                </p>
            </div>
        </div>
    </div>
</template>
