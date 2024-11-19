import { RunConfiguration } from "../RunConfiguration";
import { AlassConfiguration } from "./alass/config";
import { OpenSubtitlesConfiguration } from "./opensubtitles/config";
import { executeOpenSubtitles } from "./opensubtitles";
import { executeAlass } from "./alass";
import { Logger } from "@shared";
import { access } from "node:fs/promises";
import { constants } from "node:fs";

export enum Runners {
  FILE = "file",
  ALASS = "alass",
  OPEN_SUBTITLES = "open_subtitles",
}

const hasMovieFiles = async function (
  config: RunConfiguration,
): Promise<Error | undefined> {
  const { movie } = config;
  if (!movie) {
    return new Error("No movie file provided");
  }

  const moviePath = movie.absPath;
  try {
    await access(moviePath, constants.R_OK);
  } catch (e) {
    return e as Error;
  }

  // TODO Only SRT support for now
  const subtitlePath = `${movie.dirName}/${movie.baseName}.srt`;
  try {
    await access(subtitlePath, constants.R_OK);
  } catch (e) {
    return e as Error;
  }

  return undefined;
};

export const runModules = async function (props: {
  logger: Logger;
  config: RunConfiguration;
  alass: AlassConfiguration;
  openSubtitles: OpenSubtitlesConfiguration;
}): Promise<Readonly<Record<Runners, Error | undefined>>> {
  const { logger, config, alass, openSubtitles } = props;
  const output: Record<string, Error | undefined> = {};

  const { metadata: runMetadata } = config;
  const hasMovieError = await hasMovieFiles(config);
  if (hasMovieError) {
    output[Runners.FILE] = hasMovieError;
  } else {
    if (runMetadata.openSubtitlesRunnerVersion) {
      output[Runners.OPEN_SUBTITLES] = await executeOpenSubtitles({
        logger,
        config,
        openSubtitles,
      });
    }

    if (runMetadata.alassRunnerVersion) {
      output[Runners.ALASS] = await executeAlass({
        logger,
        config,
        alass,
      });
    }
  }

  return Object.freeze(output);
};
