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

import { Logger, TaggedLogger } from "./logger.ts";
import { FullLogData, TaggedLogData, UntaggedLogData } from "./logData.ts";
import { appName, isDev } from "../env";

export const newConsoleLogger = function (
  isEnabled: boolean = isDev(),
): Logger {
  return Object.freeze({
    log: (builder: () => UntaggedLogData) => {
      if (isEnabled) {
        const data = builder();
        console.log(appName(), data satisfies FullLogData);
      }
    },
    warn: (builder: () => UntaggedLogData) => {
      if (isEnabled) {
        const data = builder();
        console.warn(appName(), data satisfies FullLogData);
      }
    },
    error: (builder: () => UntaggedLogData) => {
      if (isEnabled) {
        const data = builder();
        console.error(appName(), data satisfies FullLogData);
      }
    },
    tag: (fileName: string, functionName: string): TaggedLogger => {
      return Object.freeze({
        log: (builder: () => TaggedLogData) => {
          if (isEnabled) {
            const data = builder();
            console.log(appName(), {
              fileName,
              functionName,
              ...data,
            } satisfies FullLogData);
          }
        },
        warn: (builder: () => TaggedLogData) => {
          if (isEnabled) {
            const data = builder();
            console.warn(appName(), {
              fileName,
              functionName,
              ...data,
            } satisfies FullLogData);
          }
        },
        error: (builder: () => TaggedLogData) => {
          if (isEnabled) {
            const data = builder();
            console.error(appName(), {
              fileName,
              functionName,
              ...data,
            } satisfies FullLogData);
          }
        },
      } satisfies TaggedLogger);
    },
  } satisfies Logger);
};
