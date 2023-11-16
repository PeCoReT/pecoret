<script>
export default {
    name: 'AuthLayout',
    props: ['title']
};
</script>

<template>
    <Toast></Toast>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <img src="/images/logo-icon.svg" alt="PeCoReT logo" class="mb-5 flex-shrink-0" />
            <div class="w-full card border-1 border-radius-extreme">
                <div class="w-full surface-card pt-5 pb-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <slot name="title">
                            <span class="text-600 font-bold" style="font-size: large">{{ title }}</span>
                        </slot>
                    </div>
                    <div>
                        <slot></slot>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.border-radius-extreme {
    border-radius: 56px;
}
</style>
