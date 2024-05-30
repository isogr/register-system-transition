#!/usr/bin/env node

import { join } from 'node:path';

import { parse as parseYAML } from 'yaml';

import { pipe, Effect, Logger } from 'effect';
import { type Types, LogLevel as EffectLogLevel } from 'effect';
import * as S from '@effect/schema/Schema';
import { NodeContext, NodeRuntime } from '@effect/platform-node';
import { FileSystem } from '@effect/platform';
import { Options, Command } from '@effect/cli';
import type { Command as Command_ } from '@effect/cli/Command';

import readdirRecursive from './readdirRecursive.mjs';


export const LogLevelSchema = S.Literal('debug', 'info', 'error', 'silent');
export type LogLevel = S.Schema.Type<typeof LogLevelSchema>
export const EFFECT_LOG_LEVELS: { [key in LogLevel]: EffectLogLevel.LogLevel } = {
  'debug': EffectLogLevel.Debug,
  'info': EffectLogLevel.Info,
  'error': EffectLogLevel.Error,
  'silent': EffectLogLevel.None,
} as const;
export const ReportingConfigSchema = S.Struct({
  logLevel: LogLevelSchema,
});


export const options = {
  registryDir: Options.directory('registry-dir'),
  outJSON: Options.file('out-json'),
  extentMap: Options.file('extent-map'),

  stakeholderGitUsername: Options.file('stakeholder-username'),
  registerVersion: Options.file('register-version'),
} as const;

export const OptionSchema = S.Struct({
  registryDir: S.String.pipe(S.nonEmpty()),
  outJSON: S.String.pipe(S.nonEmpty()),
  extentMap: S.String.pipe(S.nonEmpty()),

  stakeholderGitUsername: S.String.pipe(S.nonEmpty()),
  registerVersion: S.String.pipe(S.nonEmpty()),
});
export function parseOptions(
  rawOpts: Types.Simplify<Command_.ParseConfig<typeof options>>,
) {
  const {
    registryDir,
    outJSON,
    extentMap,
    stakeholderGitUsername,
    registerVersion,
  } = rawOpts;
  return S.decodeUnknownSync(OptionSchema)({
    registryDir,
    outJSON,
    extentMap,
    stakeholderGitUsername,
    registerVersion,
  });
}

interface ExtentMapEntry {
  name: string
  grIDs: [number] & number[]
  coordsNESW: [number, number, number, number]
}
function parseExtentLine(line: string): ExtentMapEntry {
  if (line.startsWith('[')) {
    const [idsRaw, rest] = line.slice(1).split(']');
    if (idsRaw && rest) {
      const ids = idsRaw.split(',').map(f => parseInt(f.trim(), 10));
      if (ids.length < 1) {
        throw new Error("Need at least one register item ID");
      }
      const grIDs = ids as [number] & number[]; // have at least one item
      const [e, n, w, s, ...nameParts] = rest.trim().split(/\s/);
      const coordsNESW =
        [n, e, s, w].map(c => parseInt(c!.trim(), 10)) as [number, number, number, number];
      const name = nameParts.join(' ');
      return {
        name,
        coordsNESW,
        grIDs,
      };
    } else {
      throw new Error("Invalid extent map entry");
    }
  } else if (line.trim() !== '') {
    throw new Error("Invalid extent map entry");
  } else {
    throw new Error("Empty extent map entry");
  }
}

const readRegistry = (grDataPath: string) => Effect.gen(function * (_) {
  const fs = yield * _(FileSystem.FileSystem);
  const itemPaths = yield * _(readdirRecursive(grDataPath));

  const out: Record<number, { itemData: S.Schema.Type<typeof GRItemWithExtent>, clsID: string }> =
  yield * _(Effect.reduceEffect(
    itemPaths.
    filter(p => p.endsWith('.yaml') || p.endsWith('.yml')).
    filter(p => p.indexOf('/') > 1 && !p.startsWith('extent') && !p.startsWith('proposals') && !p.startsWith('/')).
    map(path => pipe(
      fs.readFileString(join(grDataPath, path)),
      Effect.map(parseYAML),
      Effect.flatMap(S.decodeUnknown(S.Union(GRItemWithExtent), { onExcessProperty: "preserve" })),
      // Catches Schema.parse failures. We do nothing with non register items.
      Effect.catchTag(
        "ParseError",
        () => Effect.succeed(null),
        //err => Effect.logDebug(`skipping ${path} due to ${String(err)}`),
      ),
      Effect.map((out) => out && path.indexOf('/') > 0
        ? ({ [out.data.identifier]: { clsID: path.split('/')[0] as string, itemData: out } })
        : null),
    )),
    Effect.succeed({}),
    (accum, item) => ({ ...accum, ...(item ?? {}) }),
    { concurrency: 10 },
  ));

  return out;
});

const ExtentData = S.Struct({
  n: S.Number,
  e: S.Number,
  s: S.Number,
  w: S.Number,
  name: S.String.pipe(S.nonEmpty()),
});

const GRItemWithExtentData = S.Struct({
  identifier: S.Number,
  extent: ExtentData,
  extentRef: S.optional(S.UUID),
}).pipe(S.extend(S.Record(S.String, S.Unknown)));

const ItemBase = S.Struct({
  id: S.UUID,
  dateAccepted: S.String.pipe(S.nonEmpty()),
  status: S.Literal('submitted', 'valid', 'superseded', 'retired', 'invalid'),
});

const GRItemWithExtent = S.Struct({
  data: GRItemWithExtentData,
}).pipe(S.extend(ItemBase));

const GRExtentItem = S.Struct({
  data: S.Struct({
    identifier: S.Number, // 0
    name: S.String.pipe(S.nonEmpty()), // description
    extent: ExtentData,
    aliases: S.Array(S.String.pipe(S.nonEmpty())),
    informationSources: S.Array(S.Unknown), // empty
    remarks: S.String, // empty
  }),
}).pipe(S.extend(ItemBase));

const generate = (opts: S.Schema.Type<typeof OptionSchema>) => Effect.gen(function * (_) {
  const fs = yield * _(FileSystem.FileSystem);
  const itemsWithExtents = yield * _(readRegistry(opts.registryDir));
  yield * _(Effect.log(`Found ${Object.keys(itemsWithExtents).length} items with extents`));
  const extentMapFileData = yield * _(fs.readFileString(opts.extentMap));

  const proposalTS = new Date();
  const proposalTSString = proposalTS.toISOString().split('T')[0]!;

  const proposalDraft = {
    id: crypto.randomUUID(),
    justification: "Migrating extents",
    timeStarted: proposalTS,
    timeEdited: proposalTS,
    state: 'draft',
    registerVersion: opts.registerVersion,
    submittingStakeholderGitServerUsername: opts.stakeholderGitUsername,
    items: {} as Record<string, { type: 'addition' | 'clarification' }>,
  };

  const itemPayloads: Record<string, S.Schema.Type<typeof GRItemWithExtent> | S.Schema.Type<typeof GRExtentItem>> = {
  };

  for (const lineRaw of extentMapFileData.split('\n').filter(l => l.trim() !== '')) {
    const line = lineRaw.replaceAll('¬∞', '°');
    yield * _(Effect.log(`Parsing line ${line}`));
    const extentEntry = parseExtentLine(line);
    const [referenceItemID, ...otherItemIDs] = extentEntry.grIDs;
    const referenceItem = itemsWithExtents[referenceItemID];
    if (!referenceItem) {
      throw new Error(`Unable to find item with GRID ${referenceItemID}`);
    }
    const extent = referenceItem.itemData.data.extent;
    yield * _(Effect.log(`Creating extent ${JSON.stringify(extent)}`));

    let extentRef: S.Schema.Type<typeof S.UUID>;

    if (extent.name.trim().toLowerCase().replace('.', '') !== 'world') {
      extentRef = crypto.randomUUID();

      const extentPath = `/extent/${extentRef}.yaml`;
      const extentItemData: S.Schema.Type<typeof GRExtentItem> = {
        id: extentRef,
        dateAccepted: proposalTSString,
        status: 'valid',
        data: {
          identifier: 0,
          name: extentEntry.name,
          extent,
          informationSources: [],
          remarks: '',
          aliases: [],
        },
      } as const;

      itemPayloads[extentPath] = extentItemData;
      proposalDraft.items[extentPath] = { type: 'addition' };

    } else {
      // Special case—we already added World extent before
      extentRef = '538fb551-86ee-4938-96dd-710226645762';
    }

    const otherItems_ = otherItemIDs.map(grID => itemsWithExtents[grID]);
    if (otherItems_.includes(undefined)) {
      throw new Error(`Unable to find item with GRID ${otherItemIDs[otherItems_.indexOf(undefined)]}`);
    }
    const otherItems = otherItems_.map(i => i!);

    for (const item of [referenceItem, ...otherItems]) {
      const itemPath = `/${item.clsID}/${item.itemData.id}.yaml`;
      itemPayloads[itemPath] = {
        ...item.itemData,
        data: {
          ...item.itemData.data,
          extentRef,
        },
      };
      proposalDraft.items[itemPath] = { type: 'clarification' };
    }
  }

  const importableCR = {
    proposalDraft,
    itemPayloads,
  };

  yield * _(fs.writeFileString(opts.outJSON, JSON.stringify(importableCR, undefined, 4)));
});


const generateCommand = Command.
  make(
    'generate',
    options,
    (rawOpts) => pipe(
      Effect.try(() => parseOptions(rawOpts)),
      Effect.andThen((opts) => pipe(
        generate(opts),
        Logger.withMinimumLogLevel(EffectLogLevel.Debug),
      )),
    ),
  ).
  pipe(
    Command.withDescription('generate proposal that migrates extents'),
  );


const main = generateCommand.
  pipe(
    //Command.withSubcommands([watch]),
    Command.run({
      name: "Extent migration proposal generator",
      version: "N/A",
    }),
  );

Effect.
  suspend(() => main(process.argv)).
  pipe(
    Effect.provide(NodeContext.layer),
    NodeRuntime.runMain,
  );
