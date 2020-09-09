declare module 'vega-loader-arrow' {
  import type { Table } from "apache-arrow"

  // Convert arrow table to an array of proxy objects
  function arrow(data: Table | ArrayBuffer | Object[]): Object[];

  export default arrow;
}
