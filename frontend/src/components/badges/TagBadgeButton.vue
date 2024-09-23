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
            let rgb = this.label.color_rgb.replace("(", "").replace(")", "").split(",");
            let hsl = rgbToHsl(rgb[0], rgb[1], rgb[2]);
            let r = '--label-r: ' + rgb[0] + ';';
            let g = '--label-g: ' + rgb[1] + ';';
            let b = '--label-b: ' + rgb[2] + ';';
            let h = '--label-h: ' + hsl[0] + ';';
            let s = '--label-s: ' + hsl[1] + ';';
            let l = '--label-l: ' + hsl[2] + ';';
            return r + g + b + h + s + l;
        }
    }
};
</script>
<template>
    <span class="severity-badge" :style="getStyle" @click="this.$emit('click')">{{ this.label.name }}</span>
</template>
