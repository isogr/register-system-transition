import { relative, join } from 'node:path';
import { pipe, Effect } from 'effect';
import { FileSystem } from '@effect/platform';
import type { PlatformError } from '@effect/platform/Error';


export const readdirRecursive = (
  /** Directory to list. */
  dir: string,
  /**
   * Directory to output paths relative to.
   * (Don’t specify, used for recursion.)
   */
  relativeTo?: string,
):
Effect.Effect<readonly string[], PlatformError, FileSystem.FileSystem> =>
Effect.gen(function * (_) {
  const fs = yield * _(FileSystem.FileSystem);

  const dirEntries = yield * _(
    fs.readDirectory(dir),
    Effect.map(basenames => basenames.map(name => join(dir, name))),
  );

  const dirEntryStats: Record<string, FileSystem.File.Info> = yield * _(
    Effect.reduceEffect(
      dirEntries.map(path => pipe(
        fs.stat(path),
        Effect.map(stat => ({ [path]: stat })),
      )),
      Effect.succeed({}),
      (accum, item) => ({ ...accum, ...item }),
      { concurrency: 10 },
    ),
  );

  const recursiveListings = dirEntries.map(path =>
    dirEntryStats[path]?.type === 'Directory'
      ? readdirRecursive(path, relativeTo ?? dir)
      : Effect.succeed([relative(relativeTo ?? dir, path)])
    );

  const entries = yield * _(
    Effect.all(recursiveListings, { concurrency: 10 }),
    Effect.map(resultLists => resultLists.flat()),
  );

  return entries;
});


export default readdirRecursive;
