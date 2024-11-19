import { CliCommand, CliOptions } from "./command";
import { Command } from "commander";
import { asPathMeta } from "../util/path";
import { runModules } from "../module";

const FILE_NAME = "cli/exec.ts";

const handleExecCommand = async function (
  options: CliOptions,
  pathLike: string,
) {
  const { logger, downloadDirectory, metadata } = options;
  const tagged = logger.tag(FILE_NAME, "handleExecCommand");

  const pathMeta = asPathMeta(pathLike);
  const result = await runModules({
    logger,
    config: {
      downloadDirectory,
      movie: pathMeta,
      metadata,
    },
    alass: {
      inputSubtitles: "",
      outputSubtitles: "",
    },
    openSubtitles: {
      apiKey: "",
      outputSubtitles: "",
    },
  });

  for await (const [runnerType, runnerError] of Object.entries(result)) {
    if (runnerError) {
      tagged.error(() => ({
        message: `Error during module: ${runnerType}`,
        error: runnerError,
      }));
    }
  }
};

export const createExecCommand = async function (
  options: CliOptions,
): Promise<CliCommand> {
  return Object.freeze({
    addToProgram: async (program: Command) => {
      program
        .command("exec")
        .argument("path", "Path to a media file (.mp4/.mkv)")
        .action(async (pathLike) => {
          await handleExecCommand(options, pathLike);
        });
    },
  });
};
