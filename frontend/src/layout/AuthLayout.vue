<script>
export default {
    name: "AuthLayout",
    props: {
        title: {
            default: 'Sign in to continue'
        },
        hideTopTitle: {
            default: false
        },
        welcomeText: {
            default: 'Welcome to PeCoReT!'
        }
    }
}
</script>

<template>
    <Toast></Toast>
    <div class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center justify-center">
            <img src="/images/logo-icon.svg" alt="PeCoReT logo" class="mb-5 flex-shrink-0" />

            <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 33px">
                <div class="text-center mb-6" v-if="!hideTopTitle">
                    <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">{{ welcomeText }}</div>
                    <span class="text-muted-color font-medium">{{ title }}</span>
                </div>

                <div>
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>
