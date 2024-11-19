import { Command } from "commander";
import { Logger } from "@shared";
import { OutputMetadata } from "../OutputMetadata";

export interface CliOptions {
  logger: Logger;
  downloadDirectory: string;
  metadata: OutputMetadata;
}

export interface CliCommand {
  addToProgram: (program: Command) => Promise<void>;
}
