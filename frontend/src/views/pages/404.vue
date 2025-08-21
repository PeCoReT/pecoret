<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import { Button } from '@/components/ui/button';

export default {
    name: '404',
    components: { AuthLayout, Button }
};
</script>

<template>
    <AuthLayout :hide-top-title="true" title="">
        <div class="max-w-[95%] w-[95%] mx-auto">
            <div class="py-10 px-8 sm:px-20 flex flex-col items-center" style="border-radius: 53px">
                <span class="text-primary font-bold text-6xl mb-6">404</span>
                <h1 class="text-accent-foreground font-bold text-3xl lg:text-5xl mb-2">Not Found</h1>
                <div class="text-muted-foreground mb-8">Requested resource is not available.</div>

                <Button as-child>
                    <a href="/">Go to Dashboard</a>
                </Button>
            </div>
        </div>
    </AuthLayout>
</template>
