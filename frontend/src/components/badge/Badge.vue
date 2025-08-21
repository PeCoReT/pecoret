<script>
import { rgbToHsl } from '@/lib/colors';

export default {
    name: 'Badge',
    emits: ['click'],
    props: {
        color: {
            required: false
        },
        text: {
            required: true
        },
        additionalClasses: {
            default: ''
        },
        variant: {
            required: false
        }
    },
    data() {
        return {
            variants: {
                critical: '#9c1720',
                high: '#D13C0F',
                medium: '#E8971E',
                low: '#2075F5',
                informational: '#059D1D',
                open: '#3fb950',
                closed: '#ab7df8'
            }
        };
    },
    methods: {
        hexToCssProperties(color) {
            // get style based on input color
            let hex = color.replace(/^#/, '');
            // Parse the r, g, b components of the hex color
            let r = parseInt(hex.substring(0, 2), 16);
            let g = parseInt(hex.substring(2, 4), 16);
            let b = parseInt(hex.substring(4, 6), 16);
            let hsl = rgbToHsl(r, g, b);
            return `--label-r:  ${r}; --label-g: ${g}; --label-b: ${b}; --label-h: ${hsl[0]}; --label-s: ${hsl[1]}; --label-l: ${hsl[2]}`;
        }
    },
    computed: {
        getStyle() {
            if (!this.color && !this.variant) {
                return '';
            }
            if (this.variant) {
                return this.hexToCssProperties(this.variants[this.variant.toLowerCase()]);
            }
            return this.hexToCssProperties(this.color);
        }
    }
};
</script>

<template>
    <span :class="'badge box-border no-underline ' + this.additionalClasses" :style="getStyle" @click="this.$emit('click')">{{ text }}</span>
</template>

<style scoped>
.badge {
    --lightness-threshold: 0.6;
    --background-alpha: 0.18;
    --border-alpha: 0.3;
    --border-threshold: 0.96;

    --perceived-lightness: calc(((var(--label-r) * 0.2126) + (var(--label-g) * 0.7152) + (var(--label-b) * 0.0722)) / 255);
    --lightness-switch: max(0, min(calc((var(--perceived-lightness) - var(--lightness-threshold)) * -1000), 1));
    --lighten-by: calc(((var(--lightness-threshold) - var(--perceived-lightness)) * 100) * var(--lightness-switch));

    border-radius: 2em;
    display: inline-block !important;
    border: 1px solid !important;
    font-size: 12px;
    font-weight: 500;
    line-height: 18px;
    padding: 0 14px;

    border-color: hsla(var(--label-h), calc(var(--label-s) * 1%), calc((var(--label-l) + var(--lighten-by)) * 1%), var(--border-alpha)) !important;
    color: hsl(var(--label-h), calc(var(--label-s) * 1%), calc((var(--label-l) + var(--lighten-by)) * 1%)) !important;
    background: rgba(var(--label-r), var(--label-g), var(--label-b), var(--background-alpha)) !important;
}
</style>
