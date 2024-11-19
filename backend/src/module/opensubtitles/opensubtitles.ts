import { RunConfiguration } from "../../RunConfiguration";
import { OpenSubtitlesConfiguration } from "./config";
import { Logger } from "@shared";

export const executeOpenSubtitles = async function (
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _props: {
    logger: Logger;
    config: RunConfiguration;
    openSubtitles: OpenSubtitlesConfiguration;
  },
): Promise<Error | undefined> {
  return undefined;
};
