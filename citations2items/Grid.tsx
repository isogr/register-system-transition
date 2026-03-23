import React from 'react';
import {
  type TreeGridProps,
  type Column,
  TreeGrid,
} from 'react-data-grid';

import classNames from './Grid.module.css';


type Annotation =
| `color-${string}`
| 'exclamation'
| 'question'
| 'done'

type Annotations = Record<string, ReadonlySet<Annotation>>;


export const AnnotatedGrid = React.FC<Omit<TreeGridProps, 'columns'> & {
  columns: Column[],
  onChange?: undefined | ((newRows: TreeGridProps['rows']) => void),
  annotations?: undefined | Annotations,
  onAnnotate?: undefined | ((newA: Annotations) => void),
}> = function ({
  rows,
  columns,
  groupBy,
  onChange,
  annotations,
  onAnnotate,
}) {
  return <TreeGrid
    groupBy={groupBy}
    className={classNames.grid}
    rowClass={classNames.gridRow}
    headerRowClass={classNames.headerGridRow}
    columns={columns}
    rows={rows}
  />
};
