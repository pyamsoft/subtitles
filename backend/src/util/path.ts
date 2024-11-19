import { basename, dirname, extname, isAbsolute, resolve } from "node:path";

export const asPath = function (path: string): string {
  let absPath: string;
  if (isAbsolute(path)) {
    absPath = path;
  } else {
    absPath = resolve(path);
  }
  return absPath;
};

export const buildPath = function (path: string, other: string): string {
  return resolve(asPath(path), other);
};

export interface PathMeta {
  absPath: string;
  dirName: string;
  relativePath: string;
  baseName: string;
  extName: string;
}

export const asPathMeta = function (path: string): PathMeta {
  const absPath = asPath(path);
  const ext = extname(absPath);
  const baseName = basename(absPath, ext);
  return {
    absPath,
    baseName,
    dirName: dirname(absPath),
    extName: ext,
    relativePath: `${baseName}${ext}`,
  };
};
