import { Command } from "commander";
import { Logger } from "@shared";

export interface CliOptions {
  logger: Logger;
}

export interface CliCommand {
  addToProgram: (program: Command) => Promise<void>;
}
