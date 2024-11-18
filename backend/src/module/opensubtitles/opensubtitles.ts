import { RunConfiguration } from "../../RunConfiguration";
import { OpenSubtitlesConfiguration } from "./config";

export const executeOpenSubtitles = async function (
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _props: {
    config: RunConfiguration;
    openSubtitles: OpenSubtitlesConfiguration;
  },
): Promise<Error | undefined> {
  return undefined;
};
