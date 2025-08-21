/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import pinia from '../store';
import api from '@/plugins/api';
import toast from '@/plugins/toast';
import confirmPlugin from "@/plugins/confirm";


export function registerPlugins(app) {
    app.use(pinia);

    app.use(api);
    app.use(toast);

    app.use(confirmPlugin);
}
