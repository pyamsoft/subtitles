import { RunConfiguration } from "../../RunConfiguration";
import { AlassConfiguration } from "./config";
import { access } from "node:fs/promises";
import { buildPath } from "../../util/path";
import { constants } from "node:fs";
import { Logger } from "@shared";

const FILE_NAME = "alass.ts";
const ALASS_EXECUTABLE = "alass";

const hasAlassExecutable = async function (
  config: RunConfiguration,
): Promise<Error | undefined> {
  const { downloadDirectory } = config;
  if (!downloadDirectory) {
    return new Error("Empty downloadDirectory for Alass");
  }

  const executablePath = buildPath(downloadDirectory, ALASS_EXECUTABLE);
  try {
    await access(executablePath, constants.X_OK);
    return undefined;
  } catch (e) {
    return e as Error;
  }
};

export const executeAlass = async function (props: {
  logger: Logger;
  config: RunConfiguration;
  alass: AlassConfiguration;
}): Promise<Error | undefined> {
  const { logger, config } = props;

  const tagged = logger.tag(FILE_NAME, "executeAlass");

  const alassError = await hasAlassExecutable(config);

  tagged.log(() => ({
    message: `Check for Alass executable`,
    error: alassError,
  }));

  return undefined;
};
