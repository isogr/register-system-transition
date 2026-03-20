import React from 'react';


type Registry = Record<ClassID, Record<ItemID, Item>>;
type Annotation =
| `color-${string}`
| 'exclamation'
| 'question'
| 'done'

type Annotations = Record<string, ReadonlySet<Annotation>>;


const TransitionWorkspace: React.FC<Record<never, never>> =
function () {

  return (
    <>
      <ExistingInformationSources />
      <NewInformationSourceItems />
    </>
  );
}



const ExistingInformationSources:
React.FC<Record<never, never>> =
function ({ items }) {
  const [registry, storeRegistry] =
    useDB<Registry>('registry');
  const infoSources = extractInfoSources(registry);
  const [annotations, storeAnnotations] =
    useDB('existing-item-annotations');

  return infoSources
  ? <AnnotatedGrid
      items={infoSources}
      annotations={annotations}
      onAnnotate={handleAnnotate}
    />
  : <LoadPrompt onSelect={storeRegistry} />;
}


const NewInformationSourceItems:
React.FC<Record<never, never>> =
function () {
  const [annotations, storeAnnotations] =
    useDB('new-item-annotations');
  const [items, storeItems] =
    useDB<Registry>('registry');

  return (
    <AnnotatedGrid
      items={items}
      onChange={storeItems}
      annotations={annotations}
      onAnnotate={handleAnnotate}
    />
  );
}


const AnnotatedGrid = React.FC<{
}> = function ({ items, onChange, annotations, onAnnotate }) {
  return <DataGrid columns
}
