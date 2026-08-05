import { defineConfig } from "vite";
import path from "node:path";
import react from "@vitejs/plugin-react";


export default defineConfig({
    plugins: [react()],
    publicDir: "public",
    server: {
        open: "/index.html"
    },
    build: {
        outDir: "dist",
        emptyOutDir: true,
        copyPublicDir: true,
        sourcemap: true,
        rolldownOptions: {
            input: {
                main: "index.html"
            },
            output: {
                assetFileNames: "assets/[name].[ext]",
                entryFileNames: "assets/[name].js",
                chunkFileNames: "assets/[name].js"
            },
        },
        cssCodeSplit: false, 
        manifest: true, 
    },
    css: {
        preprocessorOptions: {
            scss: {
                quietDeps: true
            }
        }
    }
})