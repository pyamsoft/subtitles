import { isAbsolute, resolve } from "node:path";

export const asPath = function (path: string): string {
  let absPath: string;
  if (isAbsolute(path)) {
    absPath = path;
  } else {
    absPath = resolve(path);
  }
  return absPath;
};
