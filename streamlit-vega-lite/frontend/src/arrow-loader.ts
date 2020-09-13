import {
  ArrowTable,
} from "streamlit-component-lib";

// Forked from vega-arrow-loader for debugging/type safety/simplified type signature and support for ArrowTable.
// https://github.com/vega/vega-loader-arrow/blob/master/src/arrow.js

const RowIndex = Symbol("rowIndex");

// Convert arrow table to an array of proxy objects
export function arrow(table: ArrowTable) {
  const proxy = rowProxy(table);
  const rows = Array(table.dataRows);

  for (let i = 0, n = rows.length; i < n; ++i) {
    rows[i] = proxy(i + table.headerRows);
  }

  return rows;
}

function rowProxy(table: ArrowTable) {
  const fields: string[] = [];
  for (let i = 0; i < table.columns; i++) {
    fields.push(table.getCell(0, i).content);
  }

  const proto = {};

  fields.forEach((name, index) => {
    // skip columns with duplicate names
    if (proto.hasOwnProperty(name) || !name) return;

    Object.defineProperty(proto, name, {
      get: function () {
        return table.getCell(this[RowIndex], index).content;
      },
      set: function () {
        throw Error("Arrow field values can not be overwritten.");
      },
      enumerable: true,
    });
  });

  return (i: number) => {
    const r = Object.create(proto);
    r[RowIndex] = i;
    return r;
  };
}
