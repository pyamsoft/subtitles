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

import fastify from "fastify";
import { Logger, newConsoleLogger } from "@shared";

const FILE_NAME = "index.ts";

const main = async function (props: { logger: Logger; port?: number }) {
  const { logger, port } = props;
  const app = fastify();

  app.get("/", async (req, res) => {
    const tagged = logger.tag(FILE_NAME, "/");
    tagged.log(() => ({
      message: ["Request", req],
    }));

    tagged.log(() => ({
      message: ["Result", res],
    }));

    return {
      message: "Hello, World!",
    };
  });

  const tagged = logger.tag(FILE_NAME, "listen");
  try {
    await app.listen({
      port,
    });
  } catch (e) {
    tagged.error(() => ({
      message: "Fastify error",
      error: e,
    }));
  }
};

void (async () => {
  const logger = newConsoleLogger();
  await main({
    logger,
  });
})();
