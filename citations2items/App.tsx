import React, { createContext, useContext, useState, useMemo, useCallback, useEffect } from 'react';
import {
  fileSave,
  fileOpen,
  directoryOpen,
} from 'browser-fs-access';
import {
  type TreeDataGridProps,
  type Column,
  SelectColumn,
} from 'react-data-grid';

import {
  type Citation,
  type RegisterItem,
} from '@riboseinc/paneron-registry-kit/types';
import {
  type CommonGRItemData,
} from '@riboseinc/paneron-extension-geodetic-registry/classes/common';

import { parse as parseYAML } from 'yaml';

import classNames from './App.module.css';

import {
  Grid,
  GridContext,
  type GridContextType,
  type GridState,
} from './Grid';

import 'react-data-grid/lib/styles.css';

import 'json-diff-viewer-component';


type ItemID = string;
type GRID = string;
type CitationPositionInCitingItemsList = number;
type ClassID = string;
type CitationKey = string;

interface Registry {
  items: Record<ClassID, Record<ItemID, RegisterItem<CommonGRItemData>>>
  version: string
}
const EMPTY_REGISTRY: Registry = Object.freeze({ items: {}, version: '' } as const);


type Verdict = ['DEDUPED', CitationKey[]] | ['PREFERRED', CitationKey[]] | ['UNKNOWN', null];

interface CitationWithReferencingItems extends Citation, Record<string, unknown> {
  _verdict: Verdict;
  _ephemeralID: string;
  _citingItems: Record<GRID, CitationPositionInCitingItemsList>;
}

type InfoSourceItems = Record<CitationKey, CitationWithReferencingItems>;


const EN_COLLATOR = Intl.Collator('en');


interface RegistryContextProps {
  getItem: (grID: number) => RegisterItem<CommonGRItemData> | undefined
  clarifyValue:
    <K extends keyof Omit<Citation, 'alternateTitles'>>(
      citationKey: CitationKey,
      prop: K,
      val: Citation[K],
    ) => void,
  resetClarification:
    <K extends keyof Omit<Citation, 'alternateTitles'>>(
      citationKey: CitationKey,
      prop: K,
    ) => void,
  getPossiblyClarifiedValue:
    <K extends keyof Omit<Citation, 'alternateTitles'>>(
      citationKey: CitationKey,
      prop: K,
    ) =>
      [val: Citation[K] | undefined, edited: boolean | undefined],
}
const RegistryContext = createContext<RegistryContextProps>({
  getItem: () => undefined,
  getPossiblyClarifiedValue: () => [undefined, undefined],
  clarifyValue: () => void 0,
  resetClarification: () => void 0,
});


interface Annotations {
  deduped: Record<CitationKey, undefined | CitationKey[]>
  preferred: Record<CitationKey, undefined | CitationKey[]>
  clarified: Record<CitationKey, Partial<Citation>>
}
const INITIAL_ANNOTATIONS: Annotations = Object.freeze({
  deduped: {},
  preferred: {},
  clarified: {},
} as const);


export const TransitionWorkspace: React.FC<Record<never, never>> =
function () {

  const [registry, storeRegistry] =
    useDB<Registry>('registry', EMPTY_REGISTRY);

  //const [clarifiedItems, storeClarifiedItems] =
  //  useDB<Registry>('clarified-items', EMPTY_REGISTRY);

  const getItem = useCallback(
    function getItem(grID: number): RegisterItem<CommonGRItemData> | undefined {
      return Object.values(registry.items).
      flatMap(items => Object.values(items)).
      find(i => i.data.identifier === grID);
    },
    [registry],
  );

  const [annotations, updateAnnotations] =
    useDB<Annotations>('existing-item-annotations', INITIAL_ANNOTATIONS);

  const handleUpdateAnnotations = useCallback((newA: Annotations) => {
    const newAnnotations = { ...newA };
    for (const [key, ids] of Object.entries(newAnnotations.deduped)) {
      if (ids && ids.length < 1) {
        newAnnotations.deduped[key] = undefined;
      }
    }
    for (const [key, ids] of Object.entries(newAnnotations.preferred)) {
      if (ids && ids.length < 1) {
        newAnnotations.preferred[key] = undefined;
      }
    }
    updateAnnotations?.(newAnnotations);
  }, [updateAnnotations]);

  const [searchQ, onSearchQChange] =
    useDB<string>('search-q', '');

  const infoSources = useInfoSources(registry, annotations);

  const getPossiblyClarifiedValue = useCallback(
    function getPossiblyClarifiedValue<K extends keyof Citation>(
      citationKey: CitationKey,
      prop: K,
    ): [val: Citation[K] | undefined, edited: boolean | undefined] {
      const cit = infoSources.find(c => c._ephemeralID === citationKey);
      if (cit) {
        const clarified = annotations.clarified[citationKey];
        if (clarified?.[prop]) {
          return [
            clarified[prop],
            JSON.stringify(clarified[prop]) !== JSON.stringify(cit[prop]),
          ];
        } else {
          return [cit[prop], false];
        }
      } else {
        return [undefined, undefined];
      }
    },
    [infoSources, annotations],
  );

  const clarifyValue: RegistryContextProps['clarifyValue'] = useCallback(
    function clarifyValue(citationKey, prop, val) {
      updateAnnotations?.({
        ...annotations,
        clarified: {
          ...annotations.clarified,
          [citationKey]: {
            ...(annotations.clarified[citationKey] ?? {}),
            [prop]: val,
          },
        },
      });
    },
    [updateAnnotations, annotations],
  );

  const resetClarification: RegistryContextProps['resetClarification'] = useCallback(
    function resetClarification(citationKey, prop) {
      const citAnn = { ...(annotations.clarified[citationKey] ?? {}) };
      if (citAnn[prop]) {
        delete citAnn[prop];
      }
      updateAnnotations?.({
        ...annotations,
        clarified: {
          ...annotations.clarified,
          [citationKey]: citAnn,
        },
      });
    },
    [updateAnnotations, annotations],
  );

  const handleReset = useCallback(() => {
    localStorage.clear();
    window.location.reload();
  }, []);

  const handleDownloadWIP = useCallback(() => {
    const data = {
      registry,
      annotations,
    };
    const dataSerialized = JSON.stringify(data, null, 4);
    const encoder = new TextEncoder();
    const dataBytes = new Blob([encoder.encode(dataSerialized)]);
    fileSave(dataBytes, { fileName: 'isogr-migration-wip.json' });
  }, [registry, annotations]);

  const handleLoadWIP = useCallback(() => {
    (async () => {
      const rawData = await fileOpen();
      const decoder = new TextDecoder();
      const dataDecoded = decoder.decode(await rawData.bytes());
      const dataDeserialized = JSON.parse(dataDecoded);
      const { registry, annotations } = dataDeserialized;
      storeRegistry?.(registry);
      updateAnnotations?.(annotations);
    })();
  }, [storeRegistry, updateAnnotations]);

  const handleExportProposal = useCallback(() => {
    const sources: Record<string, Omit<CitationWithReferencingItems, '_ephemeralID'>> = {};
    for (const item of infoSources) {
      const i = { ...item };
      delete (i as any)._ephemeralID;
      const citationProperties = Object.keys(i).
        filter((k) => k !== 'alternateTitles' && !k.startsWith('_'))
      for (const prop of citationProperties) {
        const [val, maybeClarified] = getPossiblyClarifiedValue(
          item._ephemeralID,
          prop as keyof Omit<Citation, 'alternateTitles'>,
        );
        if (maybeClarified) {
          i[prop] = val;
        }
      }
      sources[item._ephemeralID] = i;
    }
    const dataSerialized = JSON.stringify(sources, null, 4);
    const encoder = new TextEncoder();
    const dataBytes = new Blob([encoder.encode(dataSerialized)]);
    fileSave(dataBytes, { fileName: 'isogr-migration-export.json' });
  }, [infoSources, getPossiblyClarifiedValue]);

  return (
    <>
      {infoSources.length > 0
        ? <Toolbar
            registry={registry}
            infoSources={infoSources}
            onReset={handleReset}
            searchQ={searchQ}
            onDownloadWIP={handleDownloadWIP}
            onExportProposal={handleExportProposal}
            onSearchQChange={onSearchQChange ?? (() => void 0)}
          />
        : storeRegistry
          ? <LoadPrompt
              onLoad={storeRegistry}
              onLoadWIP={handleLoadWIP}
              className={classNames.loadPrompt}
            />
          : <>Loading…</>}
      <RegistryContext.Provider value={{
        getItem,
        getPossiblyClarifiedValue,
        clarifyValue,
        resetClarification,
      }}>
        <InformationSources
          //onClarify={useCallback(function (item, prop, val) {
          //}, [handleUpdateAnnotations, annotations])}
          //onUndoClarify={useCallback(function (item, prop) {
          //}, [handleUpdateAnnotations, annotations])}
          onDedupe={useCallback(function (deduped, preferred) {
            handleUpdateAnnotations({
              ...annotations,
              deduped: {
                ...annotations.deduped,
                [deduped]: [
                  ...(annotations.deduped[deduped] ?? []),
                  preferred,
                ],
                [preferred]: undefined,
              },
              preferred: {
                ...annotations.preferred,
                [preferred]: [
                  ...(annotations.preferred[preferred] ?? []),
                  deduped,
                ],
                [deduped]: undefined,
              },
            })
          }, [handleUpdateAnnotations, annotations])}
          onUndoDedupe={useCallback(function (item1, item2) {
            handleUpdateAnnotations({
              ...annotations,
              deduped: {
                ...annotations.deduped,
                [item1]: (annotations.deduped[item1] ?? []).filter(i => i !== item2),
                [item2]: (annotations.deduped[item2] ?? []).filter(i => i !== item1),
              },
              preferred: {
                ...annotations.preferred,
                [item1]: (annotations.preferred[item1] ?? []).filter(i => i !== item2),
                [item2]: (annotations.preferred[item2] ?? []).filter(i => i !== item1),
              },
            })
          }, [handleUpdateAnnotations, annotations])}
          searchQ={searchQ}
          infoSources={infoSources}
        />
      </RegistryContext.Provider>
      {/*<NewInformationSourceItems />*/}
    </>
  );
}


const Toolbar: React.FC<{
  registry: Registry
  infoSources: CitationWithReferencingItems[]
  onReset: () => void
  searchQ: string,
  onSearchQChange: (q: string) => void
  onDownloadWIP: () => void
  onExportProposal: () => void
  className?: string | undefined
}> =
function ({ registry, infoSources, onReset, searchQ, onSearchQChange, onDownloadWIP, onExportProposal, className }) {
  const totalItems = useMemo((() =>
    Object.values(registry.items).flatMap(items => Object.values(items)).length
  ), [registry.items]);

  return <div className={classNames.toolbar}>
    {infoSources.length < 1
      ? <>
          Loading…
        </>
      : <>
          <div className={classNames.stats}>
            <div title="Latest accepted proposal timestamp">Register ver. {registry.version}</div>
            <div title="Total items in registry">{totalItems} items</div>
            <div title="Number of citations, shown below, after automatic de-duplication (only items where all fields are exactly the same were deduplicated automatically)">
              {infoSources.length} citations
            </div>
            <div><span className={classNames.dedupedRow}>&emsp;</span> manually de-duplicated</div>
            <div title="Other items were manually de-duplicated in favor of item of this color.">
              <span className={classNames.preferredRow}>&emsp;</span> manually preferred
            </div>
            <div><span className={classNames.clarifiedRow}>&emsp;</span> edited</div>
            <div><span className={classNames.preferredAndClarifiedRow}>&emsp;</span> preferred + edited</div>
          </div>
          <div className={classNames.actions}>
            <div>
              <input
                placeholder="exact string search…"
                value={searchQ}
                onChange={evt => onSearchQChange(evt.currentTarget.value)}
                className={searchQ !== '' ? classNames.searchEngaged : undefined}
              />
              <button onClick={() => onSearchQChange('')}>
                clear
              </button>
            </div>
            <button onClick={onDownloadWIP}>
              download work in progress
            </button>
            <button onClick={onExportProposal}>
              export result
            </button>
            <button onClick={onReset}>Restart from scratch</button>
          </div>
        </>}
  </div>
}

const InformationSources:
React.FC<{
  infoSources: CitationWithReferencingItems[]
  onDedupe: (dedupe: CitationKey, prefer: CitationKey) => void
  onUndoDedupe: (item1: CitationKey, item2: CitationKey) => void
  //onClarify: <K extends keyof Citation>(item: CitationKey, prop: K, val: Citation[K]) => void
  //onUndoClarify: <K extends keyof Citation>(item: CitationKey, prop: K) => void
  searchQ: string
  className?: string | undefined
}> =
function ({ infoSources, searchQ, onDedupe, onUndoDedupe, className }) {

  const [state, storeState] =
    useDB<GridState<CitationWithReferencingItems>>
    ('existing-item-view-state', INITIAL_GRID_STATE);

  const handleReverseSelectionOrder = useCallback(() => {
    const rows = [ ...state.selectedRows ].reverse();
    storeState?.({
      ...state,
      selectedRows: rows,
    });
  }, [storeState, state.selectedRows]);

  const rows = useMemo(() => {
    const filterFunc = searchQ.trim() !== ''
      ? ((c: CitationWithReferencingItems) =>
          Object.entries(c).
          filter(([k, ]) => !k.startsWith('_')).
          map(([, v]) => v).
          find(v => (JSON.stringify(v) ?? 'undefined').includes(searchQ))
        )
      : () => true;
    if (state.sortColumns && state.sortColumns.length > 0) {
      return [...infoSources].
      filter(filterFunc).
      sort((s1, s2) => {
        function getValString(val: number | string | string[] | null | undefined | unknown): string {
          if (typeof val === 'string') {
            return val;
          } else if (typeof val === 'number') {
            return `${val}`;
          } else if (val && (val as any[]).length) {
            return (val as any[]).map(getValString).join(', ');
          } else if (val === null) {
            return '|';
          } else if (val === undefined) {
            return '||';
          } else {
            return `${val}`;
          }
        }
        const col = state.sortColumns![0]!;
        const compareArgs: [string, string] =
          col.direction === 'ASC'
            ? [
                getValString(s1[col.columnKey]),
                getValString(s2[col.columnKey]),
              ]
            : [
                getValString(s2[col.columnKey]),
                getValString(s1[col.columnKey]),
              ];
        return EN_COLLATOR.compare(...compareArgs);
      });
    } else {
      return infoSources.filter(filterFunc);
    }
  }, [infoSources, searchQ, state.sortColumns]);

  return (
    <div className={classNames.sources}>
      {storeState
        ? <Grid<CitationWithReferencingItems>
            className={classNames.grid}
            rowKeyGetter={ROW_KEY_GETTER}
            groupBy={DEFAULT_GROUP_BY}
            columns={INFOSOURCE_COLUMNS}
            defaultColumnOptions={DEFAULT_COLUMN_OPTIONS}
            rows={rows}
            //onCellClick={(args, evt) => {
            //  //const r = Object.entries(args.row).
            //  //filter(([k]) => k !== '_citingItems' && k !== '_ephemeralID').
            //  //map(([k, v]) => ({ [k]: v })).
            //  //reduce((prev, curr) => ({ ...prev, ...curr }), {});
            //  //if (evt.metaKey) {
            //  //  console.debug("META KEY");
            //  //}
            //}}
            state={state}
            onStateChange={storeState}
          />
        : null}
      <div className={classNames.differ}>
        <Differ
          items={
            useMemo(() =>
              state.selectedRows.
              map(rID => rows.find(r => r._ephemeralID === rID)).
              filter(r => r !== undefined)
            , [rows, state.selectedRows]
             )
          }
          onSwapItems={handleReverseSelectionOrder}
          onResetDecision={onUndoDedupe}
          onDeduplicate={onDedupe}
        />
      </div>
    </div>
  );
};


const Differ: React.FC<{
  items: CitationWithReferencingItems[]
  onSwapItems: () => void
  onDeduplicate: (dedupe: string, inFavorOf: string) => void
  onResetDecision: (item1: string, item2: string) => void
  className?: string | undefined
}> = function ({ items: _items, onSwapItems, onDeduplicate, onResetDecision, className }) {
  const items: Citation[] = useMemo(() => _items.map(i => {
    const item = { ...i };
    delete (item as any)._ephemeralID;
    delete (item as any)._citingItems;
    delete (item as any)._verdict;
    return item;
  }), [_items]);

  //if (_items.length !== 2) {
  //  return <div className={classNames.differEmpty}>
  //    To de-duplicate further, select two citations.
  //  </div>;
  //}

  let actions: React.JSX.Element;

  const { getPossiblyClarifiedValue } = useContext(RegistryContext);

  const el = useMemo(() => {
    const summary = _items.length === 2
      ? {
          itemsDontHaveSameVerdict:
            (_items[0]!._verdict[0] === 'UNKNOWN')
            ||
            (_items[0]!._verdict[0] !== _items[1]!._verdict[0]),
          leftPreferredForThisItem:
            _items[1]!._verdict[0] === 'DEDUPED'
            && _items[1]!._verdict[1].includes(_items[0]!._ephemeralID),
          leftPreferredForAnyItem:
            _items[0]!._verdict[0] === 'PREFERRED',
          leftDeduped:
            _items[0]!._verdict[0] === 'DEDUPED',
          leftClarified:
            isClarified(_items[0]!, getPossiblyClarifiedValue),

          rightPreferredForThisItem:
            _items[0]!._verdict[0] === 'DEDUPED'
            && _items[0]!._verdict[1].includes(_items[1]!._ephemeralID),
          rightPreferredForAnyItem:
            _items[1]!._verdict[0] === 'PREFERRED',
          rightDeduped:
            _items[1]!._verdict[0] === 'DEDUPED',
          rightClarified:
            isClarified(_items[1]!, getPossiblyClarifiedValue),
        }
      : {
          itemsDontHaveSameVerdict: undefined,
          leftPreferredForThisItem: undefined,
          leftPreferredForAnyItem: undefined,
          leftDeduped: undefined,
          leftClarified: undefined,
          rightPreferredForThisItem: undefined,
          rightPreferredForAnyItem: undefined,
          rightDeduped: undefined,
          rightClarified: undefined,
        };

    const canChooseLeft =
         !summary.leftPreferredForThisItem
      && !summary.rightPreferredForAnyItem
      && !summary.leftDeduped
      && !summary.rightDeduped
      && !summary.rightClarified;

    const canChooseRight =
         !summary.rightPreferredForThisItem
      && !summary.leftPreferredForAnyItem
      && !summary.rightDeduped
      && !summary.leftDeduped
      && !summary.leftClarified;

    return {
      ...summary,
      canChooseLeft,
      canChooseRight,
      eligible: _items.length === 2
        && !(summary.leftDeduped && summary.rightDeduped)
        && !(summary.leftPreferredForAnyItem && summary.rightPreferredForAnyItem)
        && (canChooseLeft || canChooseRight || summary.leftPreferredForThisItem || summary.rightPreferredForThisItem),
    };
  }, [_items.length, _items[0], _items[1], getPossiblyClarifiedValue]);

  const preferRightItemTitle = el.leftPreferredForAnyItem
    ? "Other items were deduplicated in favour of the left item, so it cannot be deduplicated"
    : el.rightDeduped
      ? "Item on the right was deduplicated, so it cannot be preferred."
      : el.leftDeduped
        ? "Item on the right cannot be chosen, because item on the left was deduplicated in favor of another item."
        : el.leftClarified
          ? "Item on the right cannot be chosen, because item on the left has been clarified."
          : undefined;
  const preferLeftItemTitle = el.rightPreferredForAnyItem
    ? "Other items were deduplicated in favour of the right item, so it cannot be deduplicated"
    : el.leftDeduped
      ? "Item on the left was deduplicated, so it cannot be preferred."
      : el.rightDeduped
        ? "Item on the left cannot be chosen, because item on the right was deduplicated in favor of another item."
        : el.rightClarified
          ? "Item on the left cannot be chosen, because item on the right has been clarified."
          : undefined;

  if (el.eligible) {

    actions = (
      <>
        <button
            aria-selected={el.leftPreferredForThisItem}
            disabled={!el.canChooseLeft}
            title={preferLeftItemTitle}
            onClick={() => onDeduplicate(_items[1]!._ephemeralID, _items[0]!._ephemeralID)}>
          ⬅️ Prefer left, dedupe right ❌
        </button>
        <button onClick={onSwapItems}>
          Swap items
        </button>
        <button
            disabled={!el.leftPreferredForThisItem && !el.rightPreferredForThisItem}
            onClick={() => onResetDecision(_items[1]!._ephemeralID, _items[0]!._ephemeralID)}>
          Reset decision
        </button>
        <button
            aria-selected={el.rightPreferredForThisItem}
            disabled={!el.canChooseRight}
            title={preferRightItemTitle}
            onClick={() => onDeduplicate(_items[0]!._ephemeralID, _items[1]!._ephemeralID)}>
          ❌ Dedupe left, prefer right ➡️
        </button>
      </>
    );
  } else {
    actions = <>
      To deduplicate further, select two eligible citations.
      <div>
        {preferLeftItemTitle ? <div>{preferLeftItemTitle}</div> : null}
        {preferRightItemTitle ? <div>{preferRightItemTitle}</div> : null}
        <div>
          {el.rightDeduped && el.leftDeduped
            ? <>Both selected items were already deduplicated.</>
            : null}
        </div>
        <div>
          {el.rightPreferredForAnyItem && el.leftPreferredForAnyItem
            ? <>Both selected items are already preferred in favor of different deduplicated items.</>
            : null}
        </div>
      </div>
    </>;
  }

  return (
    <div className={classNames.differ}>
      {items.length === 2
        ? <json-diff-viewer
            className={classNames.diffViewer}
            left={items[0] ?? EMPTY_OBJECT}
            right={items[1] ?? EMPTY_OBJECT}
          />
        : null}
      <div className={classNames.diffActions}>
        {actions}
      </div>
    </div>
  );
}


const NewInformationSourceItems:
React.FC<Record<never, never>> =
function () {
  const [annotations, updateAnnotations] =
    useDB('new-item-annotations', EMPTY_OBJECT);
  const [items, storeItems] =
    useDB<readonly CitationWithReferencingItems[]>('new-items', []);
  const [state, storeState] =
    useDB<GridState<CitationWithReferencingItems>>
    ('new-item-view-state', INITIAL_GRID_STATE);

  return (
    <Grid<CitationWithReferencingItems>
      rowKeyGetter={ROW_KEY_GETTER}
      columns={INFOSOURCE_COLUMNS}
      defaultColumnOptions={DEFAULT_COLUMN_OPTIONS}
      groupBy={DEFAULT_GROUP_BY}
      rows={items}
      onChange={storeItems}
      state={state}
      onStateChange={storeState}
      annotations={annotations}
      onAnnotate={updateAnnotations}
    />
  );
};


const LoadPrompt: React.FC<{
  onLoad: (r: Registry) => void
  onLoadWIP: () => void
  className?: string | undefined
}> =
function ({ onLoad, onLoadWIP, className }) {
  const handleLoad = useCallback(async () => {
    const results: File[] = await directoryOpen({
      recursive: true,
      skipDirectory: (entry) => entry.name[0] === '.',
    });
    //const handles = result.map(b => b.handle).filter(b => b !== undefined);
    const items: Registry['items'] = {};
    const decoder = new TextDecoder();
    let latestVersion: Temporal.Instant | null = null;
    for (const res of results) {
      if (res.webkitRelativePath.includes('/proposals/') &&
          res.webkitRelativePath.endsWith('main.yaml')) {
        const proposalData = parseYAML(
          decoder.decode(
            await (new Blob([await res.arrayBuffer()])).bytes()
          )
        );
        if (proposalData.state === 'accepted') {
          console.debug(proposalData.timeDisposed);
          const date = proposalData.timeDisposed.includes('T')
            ? Temporal.Instant.from(proposalData.timeDisposed)
            : Temporal.Instant.from(`${proposalData.timeDisposed}T00:00:00.000Z`);
          if (!latestVersion) {
            latestVersion = date;
          } else if (Temporal.Instant.compare(date, latestVersion) > 0) {
            console.debug(`${date.toString()} is later than ${latestVersion.toString()}`);
            latestVersion = date;
          } else {
            console.debug(`${date.toString()} is earlier than ${latestVersion.toString()}`);
          }
        }
      }
      if (res.webkitRelativePath.includes('/gr-registry/') &&
          res.webkitRelativePath.endsWith('.yaml') &&
          !res.webkitRelativePath.endsWith('register.yaml') &&
          !res.webkitRelativePath.endsWith('panerondataset.yaml') &&
          !res.webkitRelativePath.includes('/proposals/')) {

        //console.debug(res.webkitRelativePath);

        const [_1, _2, classID, itemID] =
          res.webkitRelativePath.split('/') as [string, string, string, string];

        //console.debug({ classID, itemID });

        
         const result = parseYAML(
          decoder.decode(
            await (new Blob([await res.arrayBuffer()])).bytes()
          )
        );
        if (!result.id || !result.data) {
          console.error("Malformed registry item", result);
          throw new Error("Malformed registry item");
        }
        items[classID] ??= {};
        items[classID][itemID] = result;
      }
      //for await (const [path, file] of getFilesRecursively((res as any))) {
      //  console.debug(path);
      //  const buf = await (new Blob([await file.arrayBuffer()])).bytes();
      //}
    }
    console.debug({ items });
    onLoad({ items, version: latestVersion?.toString() ?? '' });
  }, []);
  return (
    <div className={className}>
      <button onClick={handleLoad}>
        Load GR repository root
      </button>
      <button onClick={onLoadWIP}>
        Load work in progress
      </button>
    </div>
  );
};


async function compressString(str: string) {
  const byteArray = new TextEncoder().encode(str);
  const cs = new CompressionStream('gzip');
  
  const writer = cs.writable.getWriter();
  writer.write(byteArray);
  writer.close();
  
  return JSON.stringify(
    Array.from(
      new Uint8Array(await new Response(cs.readable).arrayBuffer())
    )
  );
}

async function decompressString(compressedString: string) {
  const byteArray = new Uint8Array(JSON.parse(compressedString))
  const cs = new DecompressionStream('gzip');
  
  const writer = cs.writable.getWriter();
  writer.write(byteArray);
  writer.close();
  
  return (new TextDecoder()).decode(
    await new Response(cs.readable).arrayBuffer()
  );
}


function useDB<T extends any = unknown>
(id: string, init: T) {
  const [items, setItems] = useState<T>(init);
  const [initialized, setInitialized] = useState(false);
  useEffect(() => {
    if (!initialized) {
      async function load() {
        const maybeStored = localStorage.getItem(id);
        localStorage.removeItem(id);
        if (maybeStored) {
          console.time(`Loading & decompressing ${id}`);
          const decompressed = await decompressString(maybeStored);
          setItems(JSON.parse(decompressed));
          console.timeEnd(`Loading & decompressing ${id}`);
        }
        setInitialized(true);
      }
      load();
      return function cleanUp() {
        console.debug("Unmounting", id);
      }
    }
    return;
  }, [id, initialized, setItems]);
  useEffect(() => {
    if (initialized) {
      async function store(data: any, id: string) {
        const compressed = await compressString(JSON.stringify(data));
        console.debug("Store", id, data);
        localStorage.setItem(id, compressed);
      }
      let timeout = setTimeout(() => store(items, id), 1000);
      return function cleanUp() { clearTimeout(timeout); }
      //localStorage.setItem(id, JSON.stringify(items));
    }
    return;
  }, [id, initialized, items]);
  return [
    items,
    initialized ? ((...args) => { return setItems(...args) }) : undefined,
  ] as [
    T,
    React.Dispatch<React.SetStateAction<T>> | undefined,
  ];
}


// /**
//  * Calculate a 32 bit FNV-1a hash
//  * Found here: https://gist.github.com/vaiorabbit/5657561
//  * Ref.: http://isthe.com/chongo/tech/comp/fnv/
//  * https://stackoverflow.com/a/22429679/247441
//  *
//  * @param {string} str the input value
//  * @param {boolean} [asString=false] set to true to return the hash value as 
//  *     8-digit hex string instead of an integer
//  * @param {integer} [seed] optionally pass the hash of the previous chunk
//  * @returns {integer | string}
//  */
// function hashFnv32a(str: string, asString: false, seed?: undefined | number): number
// function hashFnv32a(str: string, asString: true, seed?: undefined | number): string
// function hashFnv32a(str: string, asString: boolean, seed?: undefined | number): string | number {
//     /*jshint bitwise:false */
//     var i, l,
//         hval = (seed === undefined) ? 0x811c9dc5 : seed;
// 
//     for (i = 0, l = str.length; i < l; i++) {
//         hval ^= str.charCodeAt(i);
//         hval += (hval << 1) + (hval << 4) + (hval << 7) + (hval << 8) + (hval << 24);
//     }
//     if( asString ){
//         // Convert to 8 digit hex string
//         return ("0000000" + (hval >>> 0).toString(16)).substr(-8);
//     }
//     return hval >>> 0;
// }

function bytesToBase64(bytes: Uint8Array) {
  const binString = Array.from(bytes, (byte) =>
    String.fromCodePoint(byte),
  ).join("");
  return btoa(binString);
}
//function base64ToBytes(base64: string) {
//  const binString = atob(base64);
//  return Uint8Array.from(binString, (m) => m.codePointAt(0) as number);
//}

function getCitationKey(c: Citation): string {
  return bytesToBase64(
    new TextEncoder().encode(
      JSON.stringify(
        Object.keys(c).
        sort(EN_COLLATOR.compare).
        reduce(
          (obj, key) => {
            const p = key as keyof Citation;
            if (c[p]) {
              if (typeof c[p] === 'string') {
                obj[p] = c[p].trim() as any;
              } else {
                obj[p] = [...c[p]].sort(EN_COLLATOR.compare).map(v => v.trim()) as any;
              }
            }
            return obj;
          },
          {} as Citation
        )
      )
    )
  );
}


function useInfoSources(
  registry: Registry,
  annotations: Annotations,
): CitationWithReferencingItems[] {
  return useMemo(() => (
    Object.values(
      Object.entries(registry.items).
      flatMap(([_classID, itemMap]) => Object.entries(itemMap).
        flatMap(([_itemUUID, item]) => item.data.informationSources.
          map((c) => ({
              ...c,
              uuid: undefined,
          })).
          map((citation, idx) => {
            const key = getCitationKey(citation);
            return {
              [key]: {
                ...citation,
                _verdict: (
                  annotations.deduped[key]
                    ? ['DEDUPED', annotations.deduped[key]]
                    : annotations.preferred[key]
                      ? ['PREFERRED', annotations.preferred[key]]
                      : ['UNKNOWN', null]
                ) as Verdict,
                _ephemeralID: key,
                _citingItems: { [`${item.data.identifier}`]: idx },
              },
            }
          })
        )
      ).
      reduce((prev, curr) => {
        //console.debug("Accumulating", { prev, curr });
        for (const [citationKey, ci] of Object.entries(curr)) {
          if (prev[citationKey]) {
            // Same citation as before, but new item
            for (const [grID, idx] of Object.entries(ci._citingItems)) {
              prev[citationKey]._citingItems[grID] = idx;
            }
          } else {
            prev[citationKey] = ci;
          }
        }
        return prev;
      }, {} as InfoSourceItems)
    )
  ), [registry, annotations]);
};


function isClarified(
  row: CitationWithReferencingItems,
  getClarified: RegistryContextProps['getPossiblyClarifiedValue'],
) {
  let clarified = false;
  for (const prop of Object.keys(row)) {
    const [, maybeClarified] = getClarified(
      row._ephemeralID,
      prop as keyof Omit<Citation, 'alternateTitles'>,
    );
    if (maybeClarified) {
      clarified = true;
      break;
    }
  }
  return clarified;
}
function getStatusClass(
  row: CitationWithReferencingItems,
  getClarified: RegistryContextProps['getPossiblyClarifiedValue'],
) {
  const clarified = isClarified(row, getClarified);
  const deduped = row._verdict[0] === 'DEDUPED';
  const preferred = row._verdict[0] === 'PREFERRED';
  return (
    deduped
      ? classNames.dedupedRow
      : preferred && clarified
        ? classNames.preferredAndClarifiedRow
        : preferred
          ? classNames.preferredRow
          : clarified
            ? classNames.clarifiedRow
            : ''
  );
};



const DEFAULT_GROUP_BY = ['title'];

const EMPTY_OBJECT = Object.freeze({} as const);

const INITIAL_GRID_STATE: GridState<CitationWithReferencingItems> = {
  expandedGroupIDs: [],
  columnWidths: {},
  groupBy: [],
  sortColumns: [],
  selectedRows: [],
  recentlyScrolledTo: undefined,
} as const;


const ROW_KEY_GETTER:
TreeDataGridProps<CitationWithReferencingItems>['rowKeyGetter'] =
r => r._ephemeralID;


const DEFAULT_COLUMN_OPTIONS = {
  //minWidth: 100,
  resizable: true,
  sortable: true,
  //draggable: true
} as const;


const RenderCell:
React.FC<{
  val: string | string[] | null | undefined
}> = function ({ val }) {
  if (val === null) {
    return <span className={classNames.valueNull}>(null)</span>;
  } else if (val === '') {
    return <span className={classNames.valueEmptyString}>(empty string)</span>;
  } else if (val === undefined) {
    return <span className={classNames.valueUndefined}>(undefined)</span>;
  } else if (typeof val === 'string') {
    return <>{val}</>;
  } else if ((val as string[]).length) {
    return <span className={classNames.valueList}>
      {(val as string[]).map(val => <RenderCell val={val} />)}
    </span>;
  } else {
    return <span className={classNames.valueError}>(error)</span>;
  }
}


const EditableField: React.FC<{
  row: CitationWithReferencingItems,
  column: { key: string },
}> =
function ({ row, column: { key } }) {
  const {
    getPossiblyClarifiedValue,
    clarifyValue,
    resetClarification,
  } = useContext(RegistryContext);
  const [val, clarified] = getPossiblyClarifiedValue(
    row._ephemeralID,
    key as keyof Omit<Citation, 'alternateTitles'>,
  );
  const [edited, setEdited] = useState<string>(val ?? '');
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    setEdited(val ?? '');
  }, [val]);

  const handleUpdateEdited = useCallback((evt: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (editing) {
      setEdited(evt.currentTarget.value);
    }
  }, [editing, setEdited]);

  const handleSaveEdited = useCallback(() => {
    if (editing && edited !== val) {
      clarifyValue(
        row._ephemeralID,
        key as keyof Omit<Citation, 'alternateTitles'>,
        edited);
      setEditing(false);
    }
  }, [row._ephemeralID, val, key, editing, edited, setEditing]);

  const handleResetClarification = useCallback(() => {
    resetClarification(
      row._ephemeralID,
      key as keyof Omit<Citation, 'alternateTitles'>,
    );
  }, [row._ephemeralID, key]);

  const deduped = row._verdict[0] === 'DEDUPED';

  return (
    <>
      {deduped
        ? <span className={classNames.value}><RenderCell val={val} /></span>
        : <>
            {editing
              ? <>
                  <textarea
                    value={edited}
                    onChange={handleUpdateEdited}
                    className={`${classNames.value} ${classNames.clarifyTextarea}`}
                  />
                  <button onClick={handleSaveEdited}>✅</button>
                </>
              : <span className={classNames.value}>
                  <RenderCell val={val} />
                </span>}
            {clarified && !editing
              ? <button onClick={handleResetClarification} title="Undo clarification">
                  ↩️
                </button>
              : null}
            <button
                title={editing
                  ? "Cancel editing"
                  : clarified
                    ? "Clarified"
                    : "Clarify"}
                onClick={() => setEditing(e => !e)}
                className={clarified && !editing ? classNames.activeEditButton : ''}>
              {editing ? "❎" : "✏️"}
            </button>
          </>}
    </>
  );
}


const INFOSOURCE_COLUMNS: Column<CitationWithReferencingItems>[] = [{
  ...SelectColumn,
  cellClass: (row) => {
    const { getPossiblyClarifiedValue } = useContext(RegistryContext);
    const getRowClass = useCallback((row: CitationWithReferencingItems) => {
      return getStatusClass(row, getPossiblyClarifiedValue);
    }, [getPossiblyClarifiedValue]);
    return getRowClass(row);
  },
}, {
  key: 'title',
  name: "Title",
  width: '30%',
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: '_citingItems',
  name: "Citing items",
  sortable: false,
  width: '10%',
  renderCell: ({ row }) => {
    const { getRow } =
    useContext<GridContextType<CitationWithReferencingItems>>
    (GridContext as any);

    const { getItem } = useContext(RegistryContext);
    const citingItemsTitle = Object.entries(row._citingItems).map(([grID, citIdx]) =>
      `#${grID} (${getItem(parseInt(grID, 10))?.data.name ?? 'item data not found'})`
      //`#${grID} (${getItem(parseInt(grID, 10))?.data.name ?? 'item data not found'}) as citation no. ${citIdx + 1}`
    ).join('\n— ');

    // after deduplication:
    const additionalCitingItems = row._verdict[0] === 'PREFERRED'
      ? row._verdict[1]!.
          flatMap(id => Object.keys(getRow(r => r._ephemeralID === id)?._citingItems ?? {}))
      : [];
    const additionalCitingItemsTitle = additionalCitingItems
      ? additionalCitingItems.map((grID) =>
          `#${grID} (${getItem(parseInt(grID, 10))?.data.name ?? 'item data not found'})`
        ).join('\n— ')
      : '';
    const deduplicationSuffix = additionalCitingItemsTitle
      ? `\nAfter manual deduplication, also by:\n— ${additionalCitingItemsTitle}`
      : row._verdict[0] === 'DEDUPED'
        ? '\nAfter manual deduplication: click “deduped info” for what these items will be citing'
        : '';

    return <span title={`Cited by (after auto-deduplication):\n— ${citingItemsTitle}${deduplicationSuffix}`}>
      {Object.keys(row._citingItems).join(', ')}
      {additionalCitingItems.length > 0 ? ` + ${additionalCitingItems.join(', ')}` : ''}
    </span>
  },
}, {
  key: '_verdict',
  name: "Verdict",
  width: 140,
  resizable: false,
  cellClass: classNames.verdictCell,
  renderCell: ({ row }) => {
    const { highlightRows } =
    useContext<GridContextType<CitationWithReferencingItems>>
    (GridContext as any);
    switch (row._verdict[0]) {
      case 'DEDUPED':
      case 'PREFERRED':
        return <>
          {row._verdict[0] === 'PREFERRED'
            ? <span className={classNames.verdictSummary}>
                + preferred
              </span>
            : <span className={classNames.verdictSummary}>
                – deduped
              </span>}
          &nbsp;
          <button
              className={classNames.verdictButton}
              onClick={() => highlightRows(row._verdict[1]!)}>
            {row._verdict[0] === 'DEDUPED' ? 'into' : 'over'}
          </button>
        </>
      case 'UNKNOWN':
        return <>no action</>
    }
  },
}, {
  key: 'author',
  name: "Author",
  width: '20%',
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'publisher',
  name: "Publisher",
  width: '20%',
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'publicationDate',
  name: "Publication date",
  width: 100,
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'revisionDate',
  name: "Revision date",
  cellClass: classNames.editableCell,
  width: 100,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'seriesIssueID',
  name: "Series issue ID",
  width: 100,
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'seriesName',
  name: "Series name",
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
  width: '20%',
}, {
  key: 'seriesPage',
  width: 100,
  name: "Series page",
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'doi',
  name: "DOI",
  width: 120,
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'uri',
  name: "URI",
  width: 120,
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'edition',
  name: "Edition",
  width: 120,
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'editionDate',
  name: "Edition date",
  width: 120,
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
}, {
  key: 'otherDetails',
  name: "Other details",
  cellClass: classNames.editableCell,
  renderCell: ({ row, column }) => <EditableField row={row} column={column} />,
  width: '20%',
}, {
  key: 'alternateTitles',
  name: "Alternate titles",
  renderCell: ({ row }) => <RenderCell val={row.alternateTitles} />,
}, {
  key: '_ephemeralID',
  name: "Ephemeral ID",
  sortable: false,
  width: 50,
}] as const;


//async function getBlobsRecursively(
//  res: Awaited<ReturnType<typeof directoryOpen>>,
//  _root?: string | undefined,
//): Promise<Record<string, Uint8Array>> {
//  const root = _root ?? '';
//  return res.flatMap((r => {
//    if (r.handle?.kind === 'file') {
//      const f = await r.handle.getFile();
//      return [{ [`${root}/${r.handle.name}`]: f }];
//    } else if (r.hasOwnProperty('directoryHandle')) {
//      (r as FileWithDirectoryAndFileHandle).directoryHandle.getDirectoryHandle();
//    }
//  });
//}

//async function * getFilesRecursively(
//  entry: FileSystemFileHandle | FileSystemDirectoryHandle,
//  _root?: string | undefined,
//): AsyncGenerator<[string, File]> {
//  const root = _root ?? '';
//  if (entry.kind === 'file') {
//    const relativePath = `${root}/${entry.name}`;
//    const file = await entry.getFile();
//    if (file !== null) {
//      yield [relativePath, file] as [string, File];
//    }
//  } else if (entry.kind === 'directory') {
//    const subEntries =
//    (entry as any).values() as AsyncGenerator<FileSystemFileHandle | FileSystemDirectoryHandle>;
//    for await (const subEntry of subEntries) {
//      yield * getFilesRecursively(subEntry, entry.name);
//    }
//  } else {
//    throw new Error("Not a valid entry");
//  }
//}

