// Forked from vega-arrow-loader for debugging/type safety/simplified type signature
// https://github.com/vega/vega-loader-arrow/blob/master/src/arrow.js

import { Table } from "apache-arrow";

const RowIndex = Symbol("rowIndex");

// Convert arrow table to an array of proxy objects
export function arrow(table: Table) {
  const proxy = rowProxy(table);
  const rows = Array(table.length);

  for (let i = 0, n = rows.length; i < n; ++i) {
    rows[i] = proxy(i);
  }

  return rows;
}

function rowProxy(table: Table) {
  const fields = table.schema.fields.map((d) => d.name);
  const proto = {};

  fields.forEach((name, index) => {
    const column = table.getColumnAt(index); // warning- can this be null?

    // skip columns with duplicate names
    if (proto.hasOwnProperty(name)) return;

    Object.defineProperty(proto, name, {
      get: function () {
        return column?.get(this[RowIndex]);
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
