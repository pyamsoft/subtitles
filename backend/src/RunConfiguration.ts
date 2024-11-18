import { OutputMetadata } from "./OutputMetadata";

export interface RunConfiguration {
  metadata: OutputMetadata;
  downloadDirectory: string;
  movie: {
    relativeFileName: string;
    directoryPath: string;
    metadata: OutputMetadata;
  };
}
