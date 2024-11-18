import { CliCommand, CliOptions } from "./command";
import { Command } from "commander";
import { asPath } from "../util/path";

const FILE_NAME = "cli/exec.ts";

export const createExecCommand = async function (
  options: CliOptions,
): Promise<CliCommand> {
  const { logger } = options;
  const tagged = logger.tag(FILE_NAME, "createExecCommand");

  return Object.freeze({
    addToProgram: async (program: Command) => {
      program
        .command("exec")
        .argument("path", "Path to a media file (.mp4/.mkv)")
        .action((pathLike) => {
          const path = asPath(pathLike);
          tagged.log(() => ({
            message: `Target path: ${path}`,
          }));
        });
    },
  });
};
