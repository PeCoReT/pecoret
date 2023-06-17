/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
//import { loadFonts } from './webfontloader'
import pinia from '../store'
import {loadApi} from "@/plugins/axios";


export function registerPlugins (app) {
  app.use(pinia)
  loadApi(app)

}
