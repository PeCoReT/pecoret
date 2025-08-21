import { fileURLToPath, URL } from 'node:url';
import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';


// https://vitejs.dev/config/
export default defineConfig({
    base: '/static/dist',
    plugins: [
        vue(),

    ],
    build: {
        manifest: 'manifest.json',
        outDir: '../server/static/dist',
        target: 'ES2022',
        emptyOutDir: true,
        rollupOptions: {
            external: ['**/.svg'],
            input: {
                full: 'src/main.js',
                css: 'src/assets/main.css.js'
            }
        }
    },
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server: {
        port: 3000,
        origin: 'http://localhost:3000'
    }
});
