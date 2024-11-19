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

import { argv } from "node:process";
import { description, name, version } from "../../package.json";
import { Logger, newConsoleLogger } from "@shared";
import { Command } from "commander";
import { createExecCommand } from "./cli/exec";
import { CliCommand } from "./cli/command";
import { OutputMetadata } from "./OutputMetadata";

const DEFAULT_DOWNLOAD_DIRECTORY = `${name}-data`;
const DEFAULT_METADATA: OutputMetadata = {
  openSubtitlesRunnerVersion: 1,
  alassRunnerVersion: 1,
};

const addToProgram = async function (program: Command, command: CliCommand) {
  await command.addToProgram(program);
};

const main = async function (props: { logger: Logger }) {
  const { logger } = props;

  const program = new Command()
    .name(name)
    .description(description)
    .version(version);

  await addToProgram(
    program,
    await createExecCommand({
      logger,
      metadata: DEFAULT_METADATA,
      downloadDirectory: DEFAULT_DOWNLOAD_DIRECTORY,
    }),
  );
  program.parse(argv);
};

void (async () => {
  const logger = newConsoleLogger();
  await main({
    logger,
  });
})();
