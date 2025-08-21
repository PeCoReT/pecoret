<script>
import { Card as CardUi, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

export default {
    name: 'Card',
    props: {
        title: {
            required: false,
            default: null
        }
    },
    components: {
        CardTitle,
        CardDescription,
        CardHeader,
        CardUi,
        CardContent,
        CardFooter
    }
};
</script>

<template>
    <CardUi class="p-6 rounded-lg">
        <!-- Conditionally render CardHeader if title is provided or 'header' slot is used -->
        <slot name="header">
            <CardHeader v-if="title || $slots.title">
                <CardTitle>
                    <slot name="title">{{ title }}</slot>
                </CardTitle>
                <CardDescription v-if="$slots.description">
                    <slot name="description"></slot>
                </CardDescription>
                <slot name="header"></slot>
                <!-- Slot for header, if needed -->
            </CardHeader>
        </slot>

        <!-- Main content slot (body of the card) -->
        <CardContent>
            <slot></slot>
            <!-- Default slot for content -->
        </CardContent>

        <!-- Conditionally render CardFooter only if 'footer' slot is used -->
        <CardFooter v-if="$slots.footer" class="flex justify-between px-6 pb-6">
            <slot name="footer"></slot>
        </CardFooter>
    </CardUi>
</template>
