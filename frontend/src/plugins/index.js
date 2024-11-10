/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import pinia from '../store';
import {loadApi} from '@/plugins/axios';
import api from '@/plugins/api';

export function registerPlugins(app) {
    app.use(pinia);

    app.use(api);
}
