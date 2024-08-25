<script>
import { rgbToHsl } from '@/utils/colors';

export default {
    name: 'TagBadgeButton',
    emits: ['click'],
    props: {
        label: {
            required: true
        }
    },
    computed: {
        getStyle() {
            if (!this.label.color_rgb) {
                return;
            }
            let hsl = rgbToHsl(this.label.color_rgb[0], this.label.color_rgb[1], this.label.color_rgb[2]);
            let r = '--label-r: ' + this.label.color_rgb[0] + ';';
            let g = '--label-g: ' + this.label.color_rgb[1] + ';';
            let b = '--label-b: ' + this.label.color_rgb[2] + ';';
            let h = '--label-h: ' + hsl[0] + ';';
            let s = '--label-s: ' + hsl[1] + ';';
            let l = '--label-l: ' + hsl[2] + ';';
            return r + g + b + h + s + l;
        }
    }
};
</script>
<template>
    <Button class="severity-badge" :style="getStyle" @click="this.$emit('click')">{{ this.label.name }}</Button>
</template>
