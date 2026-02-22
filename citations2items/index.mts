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
  citationMap: Options.file('citation-map'),

  stakeholderGitUsername: Options.file('stakeholder-username'),
  registerVersion: Options.file('register-version'),
} as const;

export const OptionSchema = S.Struct({
  registryDir: S.String.pipe(S.nonEmpty()),
  outJSON: S.String.pipe(S.nonEmpty()),
  citationMap: S.String.pipe(S.nonEmpty()),

  stakeholderGitUsername: S.String.pipe(S.nonEmpty()),
  registerVersion: S.String.pipe(S.nonEmpty()),
});
export function parseOptions(
  rawOpts: Types.Simplify<Command_.ParseConfig<typeof options>>,
) {
  const {
    registryDir,
    outJSON,
    citationMap,
    stakeholderGitUsername,
    registerVersion,
  } = rawOpts;
  return S.decodeUnknownSync(OptionSchema)({
    registryDir,
    outJSON,
    citationMap,
    stakeholderGitUsername,
    registerVersion,
  });
}

type ItemID = number;
type CitationIndex = number;
type CitationInstance = `${ItemID}-${CitationIndex}`;

interface CitationMapEntry {
  name: string
  citationRefs: [CitationInstance] & CitationInstance[]
  coordsNESW: [string, string, string, string]
}
function parseCitationLine(line: string): CitationMapEntry {
  if (line.startsWith('[')) {

    const [idsRaw, rest] = line.slice(1).split(']');
    if (idsRaw && rest) {
      const ids = idsRaw.split(' ').map(id => id.split('-').map(f => parseInt(f.trim(), 10))) as [number, number][];
      if (ids.length < 1) {
        throw new Error("Need at least one citation instance");
      }
      const citationRefs = ids.map(([itemID, citationIndex]) => `${itemID}-${citationIndex}`) as [CitationInstance] & CitationInstance[]; // have at least one item
      const [e, n, w, s, ...nameParts] = rest.trim().split(/\s/);
      const coordsNESW = [n, e, s, w] as [string, string, string, string];
      //[n, e, s, w].map(c => parseInt(c!.trim(), 10));
      const name = nameParts.join(' ');
      return {
        name,
        coordsNESW,
        citationRefs,
      };
    } else {
      throw new Error("Invalid citation map entry");
    }

  } else if (line.trim() !== '') {
    throw new Error("Invalid citation map entry");
  } else {
    throw new Error("Empty citation map entry");
  }
}

const readRegistry = (grDataPath: string) => Effect.gen(function * (_) {
  const fs = yield * _(FileSystem.FileSystem);
  const itemPaths = yield * _(readdirRecursive(grDataPath));

  const out: Record<number, { itemData: S.Schema.Type<typeof GRItemWithCitations>, clsID: string }> =
  yield * _(Effect.reduceEffect(
    itemPaths.
    filter(p => p.endsWith('.yaml') || p.endsWith('.yml')).
    filter(p => p.indexOf('/') > 1 && !p.startsWith('information-source') && !p.startsWith('proposals') && !p.startsWith('/')).
    map(path => pipe(
      fs.readFileString(join(grDataPath, path)),
      Effect.map(parseYAML),
      Effect.flatMap(S.decodeUnknown(S.Union(GRItemWithCitations), { onExcessProperty: "preserve" })),
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

const InformationSourceData = S.Struct({
  title: S.String.pipe(S.nonEmpty()),
});

const GRItemWithCitationsData = S.Struct({
  identifier: S.Number,
  informationSources: S.Array(InformationSourceData),
  informationSourceRefs: S.Array(S.String.pipe(S.nonEmpty())),
}).pipe(S.extend(S.Record(S.String, S.Unknown)));

const ItemBase = S.Struct({
  id: S.UUID,
  dateAccepted: S.String.pipe(S.nonEmpty()),
  status: S.Literal('submitted', 'valid', 'superseded', 'retired', 'invalid'),
});

const GRItemWithCitations = S.Struct({
  data: GRItemWithCitationsData,
}).pipe(S.extend(ItemBase));

const GRInformationSourceItem = S.Struct({
  data: S.Struct({
    identifier: S.Number, // 0
    name: S.String.pipe(S.nonEmpty()), // description
    aliases: S.Array(S.String.pipe(S.nonEmpty())),
    informationSources: S.Array(S.Unknown), // empty
    informationSourceRefs: S.Array(S.Unknown), // empty
    remarks: S.String, // empty
  }),
}).pipe(S.extend(ItemBase));

const generate = (opts: S.Schema.Type<typeof OptionSchema>) => Effect.gen(function * (_) {
  const fs = yield * _(FileSystem.FileSystem);
  const itemsWithCitations = yield * _(readRegistry(opts.registryDir));
  yield * _(Effect.log(`Found ${Object.keys(itemsWithCitations).length} items with citations`));
  const citationMapFileData = yield * _(fs.readFileString(opts.citationMap));

  const proposalTS = new Date();
  const proposalTSString = proposalTS.toISOString().split('T')[0]!;

  const proposalDraft = {
    id: crypto.randomUUID(),
    justification: "Migrating information sources",
    timeStarted: proposalTS,
    timeEdited: proposalTS,
    state: 'draft',
    registerVersion: opts.registerVersion,
    submittingStakeholderGitServerUsername: opts.stakeholderGitUsername,
    items: {} as Record<string, { type: 'addition' | 'clarification' }>,
  };

  const itemPayloads:
  Record<string, S.Schema.Type<typeof GRItemWithCitations> | S.Schema.Type<typeof GRInformationSourceItem>> =
  {};

  for (const lineRaw of citationMapFileData.split('\n').filter(l => l.trim() !== '')) {
    const line = lineRaw.replaceAll('¬∞', '°');
    yield * _(Effect.log(`Parsing line ${line}`));
    const infoSourceEntry = parseCitationLine(line);
    // Reference reference woo
    const [referenceRef, ...otherRefs] = infoSourceEntry.citationRefs;
    const [referenceItemID, refPosition] = referenceRef.split('-').map(f => parseInt(f, 10)) as [number, number];
    const referenceItem = itemsWithCitations[referenceItemID];
    if (!referenceItem) {
      throw new Error(`Unable to find item with GRID ${referenceItemID}`);
    }
    const referenceCitation = referenceItem.itemData.data.informationSources[refPosition];
    const informationSource = {
      // TBD
      ...referenceCitation,
      // ...citation data
    };
    yield * _(Effect.log(`Creating information source ${JSON.stringify(informationSource)}`));

    let infoSourceRef: S.Schema.Type<typeof S.UUID>;

    if (true) {
      infoSourceRef = crypto.randomUUID();

      const itemPath = `/information-source/${infoSourceRef}.yaml`;
      const itemData: S.Schema.Type<typeof GRInformationSourceItem> = {
        id: infoSourceRef,
        dateAccepted: proposalTSString,
        status: 'valid',
        data: {
          identifier: 0,
          name: infoSourceEntry.name,
          informationSources: [],
          informationSourceRefs: [],
          remarks: '',
          aliases: [],
        },
      } as const;

      itemPayloads[itemPath] = itemData;
      proposalDraft.items[itemPath] = { type: 'addition' };
    }

    const otherItems_ = otherItemIDs.map(grID => itemsWithCitations[grID]);
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
          infoSourcRef,
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
    Command.withDescription('generate proposal that migrates information sources'),
  );


const main = generateCommand.
  pipe(
    //Command.withSubcommands([watch]),
    Command.run({
      name: "Information source migration proposal generator",
      version: "N/A",
    }),
  );

Effect.
  suspend(() => main(process.argv)).
  pipe(
    Effect.provide(NodeContext.layer),
    NodeRuntime.runMain,
  );
