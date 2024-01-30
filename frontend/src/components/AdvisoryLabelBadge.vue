<template>
    <span class="severity-badge" :style="getStyle">{{ this.label.name }}</span>
</template>

<script>
export default {
    name: 'SeverityBadge',
    props: {
        label: {
            required: true
        }
    },
    methods: {
        rgbToHsl(r, g, b) {
            (r /= 255), (g /= 255), (b /= 255);
            var max = Math.max(r, g, b),
                min = Math.min(r, g, b);
            var h,
                s,
                l = (max + min) / 2;

            if (max === min) {
                h = s = 0; // achromatic
            } else {
                var d = max - min;
                s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
                switch (max) {
                    case r:
                        h = (g - b) / d;
                        break;
                    case g:
                        h = 2 + (b - r) / d;
                        break;
                    case b:
                        h = 4 + (r - g) / d;
                        break;
                }
                h *= 60;
                if (h < 0) h += 360;
            }
            return [h, s * 100, l * 100];
        }
    },
    computed: {
        getClasses() {
            return 'severity-badge';
        },

        getStyle() {
            let hsl = this.rgbToHsl(this.label.color_rgb[0], this.label.color_rgb[1], this.label.color_rgb[2]);
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
