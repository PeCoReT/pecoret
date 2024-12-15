import {usePreset} from "@primevue/themes";

export default async function loadPreset() {
    const themeModule = await import(`../presets/${window.themeName}.js`);
    usePreset(themeModule.default);
}