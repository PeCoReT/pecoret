<script>
import Toaster from '@/components/ui/toast/Toaster.vue';

export default {
    name: 'AuthLayout',
    components: { Toaster },
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
};
</script>

<template>
    <Toaster />
    <div class="bg-background flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center justify-center">
            <img alt="PeCoReT logo" class="mb-5 flex-shrink-0" src="/images/logo-icon.svg" />

            <div class="w-full bg-background text-foreground py-20 px-8 sm:px-20 card rounded-2xl">
                <div v-if="!hideTopTitle" class="text-center mb-6">
                    <div class="text-foreground text-3xl font-medium mb-4">{{ welcomeText }}</div>
                    <span class="font-medium">{{ title }}</span>
                </div>

                <div>
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>
