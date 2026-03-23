import React, { useState } from 'react';
import { Grid, type Annotations } from './Grid';


type ItemID = string;
type GRID = number;
type CitationPositionInCitingItemsList = number;
type ClassID = string;
type CitationKey = string;
type Registry = Record<ClassID, Record<ItemID, GRItem>>;
interface CitationWithReferencingItems extends Citation {
  items: Record<GRID, CitationPositionInCitingItemsList>;
}
type InfoSourceItems = Record<CitationKey, CitationWithReferencingItems>;

const TransitionWorkspace: React.FC<Record<never, never>> =
function () {

  return (
    <>
      <ExistingInformationSources />
      <NewInformationSourceItems />
    </>
  );
}


function useDB<T extends any = any>(id: string, init: T) {
  const [items, setItems] = useState<T>(init);
  return [items, setItems];
}


function getCitationKey(c: Citation): string {
  return JSON.stringify(c);
}


function useInfoSources(registry: Registry): InfoSourceItems {
  return Object.entries(registry).
    flatMap(([classID, itemMap]) => Object.entries(itemMap).
      flatMap(([itemUUID, item]) => item.informationSources.
        map((citation, idx) => ({
          [getCitationKey(citation)]: {
            ...citation,
            items: { [item.identifier]: idx },
          },
        }))
      )
    ).
    reduce((prev, curr) => {
      for (const [citationKey, ci] of Object.entries(curr)) {
        if (prev[citationKey]) {
          // Same citation as before, but new item
          for (const [grID, idx] of Object.entries(ci.items)) {
            prev[citationKey].items[grID] = idx;
          }
        } else {
          prev[citationKey] = ci;
        }
      }
      return prev;
    }, {} as InfoSourceItems);
}



const ExistingInformationSources:
React.FC<Record<never, never>> =
function ({ items }) {
  const [registry, storeRegistry] =
    useDB<Registry>('registry', {});
  const infoSources = useInfoSources(registry);
  const [annotations, updateAnnotations] =
    useDB('existing-item-annotations', {});
  const [state, storeState] =
    useDB('existing-item-view-state', {});

  return infoSources
  ? <AnnotatedGrid
      rowKeyGetter={ROW_KEY_GETTER}
      columns={INFOSOURCE_COLUMNS}
      items={infoSources}
      annotations={annotations}
      onAnnotate={updateAnnotations}
    />
  : <LoadPrompt onSelect={storeRegistry} />;
}


const NewInformationSourceItems:
React.FC<Record<never, never>> =
function () {
  const [annotations, updateAnnotations] =
    useDB('new-item-annotations', {});
  const [items, storeItems] =
    useDB<InfoSourceItems>('new-items', {});
  const [state, storeState] =
    useDB('new-item-view-state', {});

  return (
    <AnnotatedGrid
      rowKeyGetter={ROW_KEY_GETTER}
      columns={INFOSOURCE_COLUMNS}
      items={items}
      onChange={storeItems}
      annotations={annotations}
      onAnnotate={updateAnnotations}
    />
  );
}


const ROW_KEY_GETTER: TreeGridProps['rowKeyGetter'] = r => r.id;

const INFOSOURCE_COLUMNS: Column = Object.freeze([{
  key: 'title',
  name: "Title",
}, {
  key: 'alternateTitles',
  name: "Alternate titles",
}, {
  key: 'author',
  name: "Author",
}, {
  key: 'publisher',
  name: "Publisher",
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
}, {
  key: 'doi',
  name: "DOI",
}, {
  key: 'uri',
  name: "URI",
}] as const);
