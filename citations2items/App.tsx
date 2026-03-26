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

type Verdict = ['DEDUPED', CitationKey[]] | ['PREFERRED', CitationKey[]] | ['UNKNOWN', null];

interface CitationWithReferencingItems extends Citation, Record<string, unknown> {
  _verdict: Verdict;
  _ephemeralID: string;
  _citingItems: Record<GRID, CitationPositionInCitingItemsList>;
}

type InfoSourceItems = Record<CitationKey, CitationWithReferencingItems>;


const EN_COLLATOR = Intl.Collator('en');


const RegistryContext = createContext<{
  getItem: (grID: number) => RegisterItem<CommonGRItemData> | undefined
}>({
  getItem: () => undefined,
});


const EMPTY_REGISTRY = Object.freeze({ items: {}, version: '' } as const);


export const TransitionWorkspace: React.FC<Record<never, never>> =
function () {

  const [registry, storeRegistry] =
    useDB<Registry>('registry', EMPTY_REGISTRY);

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

  const handleReset = useCallback(() => {
    localStorage.clear();
    window.location.reload();
  }, []);

  const handleDownloadWIP = useCallback(() => {
    const data = {
      registry: JSON.parse(localStorage.getItem('registry') ?? ''),
      annotations: JSON.parse(localStorage.getItem('existing-item-annotations') ?? ''),
    };
    const dataSerialized = JSON.stringify(data, null, 4);
    const encoder = new TextEncoder();
    const dataBytes = new Blob([encoder.encode(dataSerialized)]);
    fileSave(dataBytes, { fileName: 'isogr-migration-wip.json' });
  }, []);

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
  }, []);

  return (
    <>
      {infoSources.length > 0
        ? <Toolbar
            registry={registry}
            infoSources={infoSources}
            onReset={handleReset}
            searchQ={searchQ}
            onDownloadWIP={handleDownloadWIP}
            onLoadWIP={handleLoadWIP}
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
      <RegistryContext.Provider value={{ getItem }}>
        <InformationSources
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
  onLoadWIP: () => void
  onExportProposal: () => void
  className?: string | undefined
}> =
function ({ registry, infoSources, onReset, searchQ, onSearchQChange, onDownloadWIP, onLoadWIP, onExportProposal, className }) {
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
            <div>Register version (latest proposal) {registry.version}</div>
            <div>{totalItems} items</div>
            <div>{infoSources.length} de-duplicated citations</div>
            <button onClick={onReset}>Restart from scratch</button>
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
            <button disabled onClick={onExportProposal}>
              export proposal
            </button>
          </div>
        </>}
  </div>
}


interface Annotations {
  deduped: Record<CitationKey, undefined | CitationKey[]>
  preferred: Record<CitationKey, undefined | CitationKey[]>
}

const INITIAL_ANNOTATIONS: Annotations = Object.freeze({
  deduped: {},
  preferred: {},
} as const);

const InformationSources:
React.FC<{
  infoSources: CitationWithReferencingItems[]
  onDedupe: (dedupe: CitationKey, prefer: CitationKey) => void
  onUndoDedupe: (item1: CitationKey, item2: CitationKey) => void
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
      <Grid<CitationWithReferencingItems>
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

  if (items.length === 2) {
    const leftPreferredForThisItem =
      _items[1]!._verdict[0] === 'DEDUPED'
      && _items[1]!._verdict[1].includes(_items[0]!._ephemeralID);
    const leftPreferredForAnyItem =
      _items[0]!._verdict[0] === 'PREFERRED';
    const leftDeduped =
      _items[0]!._verdict[0] === 'DEDUPED';

    const rightPreferredForThisItem =
      _items[0]!._verdict[0] === 'DEDUPED'
      && _items[0]!._verdict[1].includes(_items[1]!._ephemeralID);
    const rightPreferredForAnyItem =
      _items[1]!._verdict[0] === 'PREFERRED';
    const rightDeduped =
      _items[1]!._verdict[0] === 'DEDUPED';

    const canChooseLeft =
      !leftPreferredForThisItem
      && !rightPreferredForAnyItem
      && !leftDeduped
      && !rightDeduped;
    const canChooseRight =
      !rightPreferredForThisItem
      && !leftPreferredForAnyItem
      && !rightDeduped
      && !leftDeduped;

    actions = (
      <>
        <button
            aria-selected={leftPreferredForThisItem}
            disabled={!canChooseLeft}
            title={rightPreferredForAnyItem
              ? "Other items were deduplicated in favour of the right item, so it cannot be deduplicated"
              : leftDeduped
                ? "Item on the left was deduplicated, so it cannot be preferred."
                : rightDeduped
                  ? "Item on the right was already deduplicated."
                  : undefined}
            onClick={() => onDeduplicate(_items[1]!._ephemeralID, _items[0]!._ephemeralID)}>
          ⬅️ Prefer left, dedupe right ❌
        </button>
        <button onClick={onSwapItems}>
          Swap items
        </button>
        <button
            disabled={!leftPreferredForThisItem && !rightPreferredForThisItem}
            onClick={() => onResetDecision(_items[1]!._ephemeralID, _items[0]!._ephemeralID)}>
          Reset decision
        </button>
        <button
            aria-selected={rightPreferredForThisItem}
            disabled={!canChooseRight}
            title={leftPreferredForAnyItem
              ? "Other items were deduplicated in favour of the left item, so it cannot be deduplicated"
              : rightDeduped
                ? "Item on the right was deduplicated, so it cannot be preferred."
                : leftDeduped
                  ? "Item on the left was already deduplicated."
                  : undefined}
            onClick={() => onDeduplicate(_items[0]!._ephemeralID, _items[1]!._ephemeralID)}>
          ❌ Dedupe left, prefer right ➡️
        </button>
      </>
    );
  } else {
    actions = <>To deduplicate further, select two citations.</>;
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


function useDB<T extends any = unknown>
(id: string, init: T) {
  const [items, setItems] = useState<T>(init);
  const [initialized, setInitialized] = useState(false);
  useEffect(() => {
    if (!initialized) {
      const maybeStored = localStorage.getItem(id);
      localStorage.removeItem(id);
      if (maybeStored) {
        console.debug("Load", id, JSON.parse(maybeStored));
        setItems(JSON.parse(maybeStored));
      }
      setInitialized(true);
    }
  }, [id, initialized, setItems]);
  useEffect(() => {
    if (initialized) {
      console.debug("Store", id, items);
      localStorage.setItem(id, JSON.stringify(items));
    }
  }, [id, initialized, items]);
  return [items, initialized ? ((...args) => { return setItems(...args) }) : undefined] as [
    T,
    React.Dispatch<React.SetStateAction<T>> | undefined,
  ];
}


function getCitationKey(c: Citation): string {
  return JSON.stringify(Object.keys(c).sort(EN_COLLATOR.compare).reduce(
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
  ), null, 4);
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


const INFOSOURCE_COLUMNS: Column<CitationWithReferencingItems>[] = [
  SelectColumn, {
  key: 'title',
  name: "Title",
  width: '30%',
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
      ? `\nAfter deduplication, also by:\n— ${additionalCitingItemsTitle}`
      : row._verdict[0] === 'DEDUPED'
        ? '\n(before deduplication; click “show preferred” for what these items will be citing after)'
        : '';

    return <span title={`Cited by:\n— ${citingItemsTitle}${deduplicationSuffix}`}>
      {Object.keys(row._citingItems).join(', ')}
      {additionalCitingItems.length > 0 ? ` + ${additionalCitingItems}` : ''}
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
                ✅
              </span>
            : <span className={classNames.verdictSummary}>
                🟠
              </span>}
          &nbsp;
          <button
              className={classNames.verdictButton}
              onClick={() => highlightRows(row._verdict[1]!)}>
            show {row._verdict[0] === 'DEDUPED' ? 'preferred' : 'deduped'}
          </button>
        </>
      case 'UNKNOWN':
        return <>no action</>
    }
  },
}, {
  key: 'author',
  name: "Author",
  renderCell: ({ row }) => <RenderCell val={row.author} />,
  width: '20%',
}, {
  key: 'publisher',
  name: "Publisher",
  renderCell: ({ row }) => <RenderCell val={row.publisher} />,
  width: '20%',
}, {
  key: 'publicationDate',
  name: "Publication date",
  renderCell: ({ row }) => <RenderCell val={row.publicationDate} />,
}, {
  key: 'revisionDate',
  name: "Revision date",
  renderCell: ({ row }) => <RenderCell val={row.revisionDate} />,
}, {
  key: 'seriesIssueID',
  name: "Series issue ID",
  width: 80,
  renderCell: ({ row }) => <RenderCell val={row.seriesIssueID} />,
}, {
  key: 'seriesName',
  name: "Series name",
  renderCell: ({ row }) => <RenderCell val={row.seriesName} />,
  width: '20%',
}, {
  key: 'seriesPage',
  width: 80,
  name: "Series page",
  renderCell: ({ row }) => <RenderCell val={row.seriesPage} />,
}, {
  key: 'doi',
  name: "DOI",
  width: 100,
  renderCell: ({ row }) => <RenderCell val={row.doi} />,
}, {
  key: 'uri',
  name: "URI",
  width: 100,
  renderCell: ({ row }) => <RenderCell val={row.uri} />,
}, {
  key: 'edition',
  name: "Edition",
  renderCell: ({ row }) => <RenderCell val={row.edition} />,
}, {
  key: 'editionDate',
  name: "Edition date",
  renderCell: ({ row }) => <RenderCell val={row.editionDate} />,
}, {
  key: 'otherDetails',
  name: "Other details",
  renderCell: ({ row }) => <RenderCell val={row.otherDetails} />,
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

