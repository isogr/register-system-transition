import React, { createContext, useRef, useEffect, useCallback, useMemo } from 'react';
import {
  type TreeDataGridProps,
  type Column,
  type DataGridHandle,
  TreeDataGrid,
} from 'react-data-grid';

import classNames from './Grid.module.css';


type Annotation =
| `color-${string}`
| 'exclamation'
| 'question'
| 'done'

type Annotations = Record<string, ReadonlySet<Annotation>>;

export interface GridState<T> {
  expandedGroupIDs: readonly string[]
  groupBy: readonly string[]
  columnWidths: Readonly<Record<string, { type: 'resized' | 'measured', width: number }>>
  sortColumns: TreeDataGridProps<T>['sortColumns']
  selectedRows: readonly string[]
  recentlyScrolledTo: T | undefined
}


export interface GridContextType<T> {
  highlightRows: (rID: string[]) => void
  getRow: (test: (r: T) => boolean) => T | undefined
}
export const GridContext = createContext<GridContextType<unknown>>({
  highlightRows: () => void 0,
  getRow: () => undefined,
});


interface GridProps<T>
  extends Omit<TreeDataGridProps<T>,
    | 'columns'
    | 'rowGrouper'
    | 'groupBy'
    | 'expandedGroupIds'
    | 'onExpandedGroupIdsChange'
  > {
  columns: Column<T>[],
  onChange?: undefined | ((newRows: TreeDataGridProps<T>['rows']) => void),
  annotations?: undefined | Annotations,
  onAnnotate?: undefined | ((newA: Annotations) => void),
  state: GridState<T>,
  onStateChange?: undefined | ((newS: GridState<T>) => void),

  groupBy?: undefined | TreeDataGridProps<T>['groupBy'],
  rowGrouper?: undefined | TreeDataGridProps<T>['rowGrouper'],
}

export function Grid<T>({
  rows,
  columns,
  groupBy,
  rowGrouper,
  onChange,
  annotations,
  onAnnotate,
  state,
  onStateChange,
  ...props
}: GridProps<T>) {
  const ref = useRef<DataGridHandle>(null);

  const keyGetter = props.rowKeyGetter ?? ((r: T) => (r as any).id);

  const defaultGrouper: TreeDataGridProps<T>['rowGrouper'] = useCallback((rows, cKey) => {
    const out = Object.groupBy(rows, (row) => {
      const v = row[cKey as keyof T];
      return typeof v === 'string' ? v : `${v}`;
    }) as Record<string, T[]>;
    return out;
  }, [rows]);

  //useEffect(() => {
  //  if (state.selectedRows.length > 0) {
  //    if (state.selectedRows.find(rID => !rows.find(r => keyGetter(r) === rID))) {
  //      onStateChange?.({
  //        ...state,
  //        selectedRows: state.selectedRows.filter
  //      });
  //    }
  //  }
  //}, [state]);

  function highlightRows(rIDs: string[]) {
    if (rIDs.length < 1) {
      return;
    }
    const rowIdx = rows.findIndex(r => keyGetter(r) === rIDs[0]!);
    onStateChange?.({
      ...state,
      selectedRows: rIDs.
      map(rID => keyGetter(rows.find(r => keyGetter(r) === rID)!) as string).
      filter(r => !!r),
    });
    if (rowIdx >= 0) {
      ref.current?.scrollToCell({ rowIdx });
    }
  }

  function getRow(check: (r: T) => boolean): T | undefined {
    return rows.find(r => check(r));
  }

  //const defaultGroupBy: TreeDataGridProps<T>['groupBy'] = useMemo(() => {
  //  return [];
  //}, []);

  return <GridContext.Provider value={{ highlightRows, getRow }}>
    <TreeDataGrid<T>
      ref={ref}
      groupBy={state.groupBy}
      rowGrouper={rowGrouper ?? defaultGrouper}
      //rowClass={useCallback((row => { console.debug(row._ephemeralID, state.recentlyScrolledTo?._ephemeralID); return state.recentlyScrolledTo
      //  ? keyGetter(state.recentlyScrolledTo) === keyGetter(row)
      //    ? classNames.recentlyScrolledTo
      //    : undefined
      //  : undefined
      //}), [state.recentlyScrolledTo])}
      columnWidths={useMemo(() =>
        new Map(Object.entries(state.columnWidths)),
        [state.columnWidths],
      )}
      onColumnWidthsChange={useCallback((columnWidths) => {
        onStateChange?.({
          ...state,
          columnWidths: columnWidths.
          entries().
          map(([key, value]) => ({ [key]: value })).
          reduce((p, c) => ({ ...p, ...c}), {}),
        });
      }, [state, onStateChange])}
      sortColumns={state.sortColumns}
      onSortColumnsChange={(sortColumns) => {
        onStateChange?.({
          ...state,
          sortColumns: sortColumns.length > 0 ? [sortColumns[0]!] : [],
        });
      }}
      expandedGroupIds={useMemo(() => new Set(state.expandedGroupIDs), [state.expandedGroupIDs])}
      onExpandedGroupIdsChange={useCallback((ids) => {
        onStateChange?.({
          ...state,
          expandedGroupIDs: Array.from(ids.values()) as string[]
        })
      }, [state, onStateChange])}
      className={classNames.grid}
      headerRowClass={classNames.headerGridRow}
      columns={columns}
      rows={rows}
      selectedRows={useMemo(() => new Set(state.selectedRows), [state.selectedRows])}
      onSelectedRowsChange={useCallback((rows) => {
        console.debug('onstatechange onselectrowschange');
        onStateChange?.({
          ...state,
          selectedRows: Array.from(rows.values()) as string[],
        });
      }, [state, onStateChange])}
      {...props}
    />
  </GridContext.Provider>
};
