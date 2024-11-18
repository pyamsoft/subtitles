/*
 * Copyright 2024 pyamsoft
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { defineConfig } from "vite";
import { resolve } from "node:path";

const root = resolve(__dirname, "..");

export default defineConfig((env) => {
  const isDev = env.mode !== "production";
  return {
    build: {
      ssr: resolve(root, "backend", "src", "index.ts"),
      outDir: "dist",
      rollupOptions: {
        input: resolve(root, "backend", "src", "index.ts"),
        output: {
          entryFileNames: (chunk) => {
            if (chunk.name === "index") {
              return "[name].js";
            }

            return "[name]-[hash].js";
          },
        },
      },
      minify: !isDev,
      sourcemap: isDev,
    },
    resolve: {
      alias: {
        "@shared": resolve(root, "shared", "src"),
      },
    },
  };
});
