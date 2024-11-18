import { RunConfiguration } from "../RunConfiguration";
import { AlassConfiguration } from "./alass/config";
import { OpenSubtitlesConfiguration } from "./opensubtitles/config";
import { executeOpenSubtitles } from "./opensubtitles";
import { executeAlass } from "./alass";

export enum Runners {
  ALASS = "alass",
  OPEN_SUBTITLES = "open_subtitles",
}

export const runModules = async function (props: {
  config: RunConfiguration;
  alass: AlassConfiguration;
  openSubtitles: OpenSubtitlesConfiguration;
}): Promise<Readonly<Record<Runners, Error | undefined>>> {
  const { config, alass, openSubtitles } = props;
  const output: Record<string, Error | undefined> = {};

  const { movie, metadata: runMetadata } = config;
  const { metadata: movieMetadata } = movie;

  if (
    runMetadata.openSubtitlesRunnerVersion >
    movieMetadata.openSubtitlesRunnerVersion
  ) {
    output[Runners.OPEN_SUBTITLES] = await executeOpenSubtitles({
      config,
      openSubtitles,
    });
  }

  if (runMetadata.alassRunnerVersion > movieMetadata.alassRunnerVersion) {
    output[Runners.ALASS] = await executeAlass({
      config,
      alass,
    });
  }

  return Object.freeze(output);
};
