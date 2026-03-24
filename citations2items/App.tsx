import React, { createContext, useContext, useState, useMemo, useCallback, useEffect } from 'react';
import {
  fileSave,
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
  ScrollToCellContext,
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

  const [searchQ, onSearchQChange] =
    useDB<string>('search-q', '');

  const infoSources = useInfoSources(registry, annotations);

  const handleReset = useCallback(() => {
    localStorage.clear();
    window.location.reload();
  }, []);

  return (
    <>
      {infoSources.length > 0
        ? <Toolbar
            registry={registry}
            infoSources={infoSources}
            onReset={handleReset}
            searchQ={searchQ}
            onSearchQChange={onSearchQChange ?? (() => void 0)}
          />
        : storeRegistry
          ? <LoadPrompt
              onLoad={storeRegistry}
              className={classNames.loadPrompt}
            />
          : <>Loading…</>}
      <RegistryContext.Provider value={{ getItem }}>
        <ExistingInformationSources
          onDedupe={useMemo(() => function (deduped, preferred) {
            updateAnnotations?.({
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
          }, [updateAnnotations, annotations])}
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
  className?: string | undefined
}> =
function ({ registry, infoSources, onReset, searchQ, onSearchQChange, className }) {
  const totalItems = useMemo((() =>
    Object.values(registry.items).flatMap(items => Object.values(items)).length
  ), [registry.items]);
  return <div className={classNames.toolbar}>
    {infoSources.length < 1
      ? <>Please select the root directory of GR repository first</>
      : <>
          <div className={classNames.actions}>
          </div>
          <div className={classNames.stats}>
            <div>Register version (latest proposal) {registry.version}</div>
            <div>{totalItems} items</div>
            <div>{infoSources.length} de-duplicated citations</div>
            <button onClick={onReset}>Restart from scratch</button>
            <input value={searchQ} onChange={evt => onSearchQChange(evt.currentTarget.value)} />
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

const ExistingInformationSources:
React.FC<{
  infoSources: CitationWithReferencingItems[]
  onDedupe: (dedupe: CitationKey, prefer: CitationKey) => void
  className?: string | undefined
}> =
function ({ infoSources, onDedupe, className }) {

  const [state, storeState] =
    useDB<GridState<CitationWithReferencingItems>>
    ('existing-item-view-state', INITIAL_GRID_STATE);

  const rows = useMemo(() => {
    if (state.sortColumns && state.sortColumns.length > 0) {
      return [...infoSources].sort((s1, s2) => {
        const col = state.sortColumns![0]!;
        const compareArgs: [string, string] =
          col.direction === 'ASC'
            ? [
                `${s1[col.columnKey as keyof CitationWithReferencingItems]}`,
                `${s2[col.columnKey as keyof CitationWithReferencingItems]}`,
              ]
            : [
                `${s2[col.columnKey as keyof CitationWithReferencingItems]}`,
                `${s1[col.columnKey as keyof CitationWithReferencingItems]}`,
              ];
        return EN_COLLATOR.compare(...compareArgs);
      });
    } else {
      return infoSources;
    }
  }, [infoSources, state.sortColumns]);

  return <div className={classNames.sources}>
    <Grid<CitationWithReferencingItems>
      className={classNames.grid}
      rowKeyGetter={ROW_KEY_GETTER}
      groupBy={DEFAULT_GROUP_BY}
      columns={INFOSOURCE_COLUMNS}
      defaultColumnOptions={DEFAULT_COLUMN_OPTIONS}
      rows={rows}
      onCellClick={(args, evt) => {
        //const r = Object.entries(args.row).
        //filter(([k]) => k !== '_citingItems' && k !== '_ephemeralID').
        //map(([k, v]) => ({ [k]: v })).
        //reduce((prev, curr) => ({ ...prev, ...curr }), {});
        //if (evt.metaKey) {
        //  console.debug("META KEY");
        //}
      }}
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
        onDeduplicate={onDedupe}
      />
    </div>
  </div>
};


const Differ: React.FC<{
  items: CitationWithReferencingItems[]
  onDeduplicate: (dedupe: string, inFavorOf: string) => void
  className?: string | undefined
}> = function ({ items: _items, onDeduplicate, className }) {
  const items: Citation[] = useMemo(() => _items.map(i => {
    const item = { ...i };
    delete (item as any)._ephemeralID;
    delete (item as any)._citingItems;
    delete (item as any)._verdict;
    return item;
  }), [_items]);

  if (_items.length !== 2) {
    return <div className={classNames.differEmpty}>
      To de-duplicate further, select two citations.
    </div>;
  }

  const leftPreferred =
    _items[1]!._verdict[0] === 'DEDUPED'
    && _items[1]!._verdict[1].includes(_items[0]!._ephemeralID);
  const rightPreferred =
    _items[0]!._verdict[0] === 'DEDUPED'
    && _items[0]!._verdict[1].includes(_items[1]!._ephemeralID);

  return (
    <div className={classNames.differ}>
      <json-diff-viewer
        className={classNames.diffViewer}
        left={items[0] ?? EMPTY_OBJECT}
        right={items[1] ?? EMPTY_OBJECT}
      />
      <div className={classNames.diffActions}>
        <button
            aria-selected={leftPreferred}
            disabled={leftPreferred}
            onClick={() => onDeduplicate(_items[1]!._ephemeralID, _items[0]!._ephemeralID)}>
          Prefer left
        </button>
        <button
            aria-selected={rightPreferred}
            disabled={rightPreferred}
            onClick={() => onDeduplicate(_items[0]!._ephemeralID, _items[1]!._ephemeralID)}>
          Prefer right
        </button>
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
  className?: string | undefined
}> =
function ({ onLoad, className }) {
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
    <button onClick={handleLoad} className={className}>
      Load GR repository root
    </button>
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


const INFOSOURCE_COLUMNS: Column<CitationWithReferencingItems>[] = [
  SelectColumn, {
  key: 'title',
  name: "Title",
  width: '30%',
}, {
  key: '_citingItems',
  name: "Citing items",
  width: '10%',
  renderCell: ({ row }) => {
    const { getItem } = useContext(RegistryContext);
    const citingItems = Object.entries(row._citingItems).map(([grID, citIdx]) =>
      `#${grID} (${getItem(parseInt(grID, 10))?.data.name ?? 'item data not found'}) as citation no. ${citIdx}`
    ).join('\n— ')
    return <span title={`Cited by:\n— ${citingItems}`}>
      {Object.keys(row._citingItems).join(', ')}
    </span>
  },
}, {
  key: '_verdict',
  name: "Verdict",
  renderCell: ({ row }) => {
    const { highlightRows } = useContext(ScrollToCellContext);
    switch (row._verdict[0]) {
      case 'DEDUPED':
      case 'PREFERRED':
        return <>
          {row._verdict[0] === 'PREFERRED' ? <>✅</> : <>🟠</>}
          &nbsp;
          <button onClick={() => highlightRows(row._verdict[1]!)}>
            show {row._verdict[0] === 'DEDUPED' ? 'preferred' : 'deduped'}
          </button>
        </>
      case 'UNKNOWN':
        return <>no action</>
    }
  },
}, {
  key: 'alternateTitles',
  name: "Alternate titles",
  renderCell: ({ row }) => <>{(row.alternateTitles ?? []).join(', ')}</>,
}, {
  key: 'author',
  name: "Author",
  width: '20%',
}, {
  key: 'publisher',
  name: "Publisher",
  width: '20%',
}, {
  key: 'publicationDate',
  name: "Publication date",
}, {
  key: 'revisionDate',
  name: "Revision date",
}, {
  key: 'seriesIssueID',
  name: "Series issue ID",
}, {
  key: 'seriesName',
  name: "Series name",
  width: '20%',
}, {
  key: 'seriesPage',
  name: "Series page",
}, {
  key: 'edition',
  name: "Edition",
}, {
  key: 'editionDate',
  name: "Edition date",
}, {
  key: 'otherDetails',
  name: "Other details",
  width: '20%',
}, {
  key: 'doi',
  name: "DOI",
}, {
  key: 'uri',
  name: "URI",
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

