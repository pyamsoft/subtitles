import { OutputMetadata } from "./OutputMetadata";
import { PathMeta } from "./util/path";

export interface RunConfiguration {
  metadata: OutputMetadata;
  downloadDirectory: string;
  movie: PathMeta;
}
