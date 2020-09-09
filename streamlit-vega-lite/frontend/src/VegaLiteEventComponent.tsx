import React, { useEffect, useMemo } from "react"
import {
  withStreamlitConnection,
  Streamlit,
  ArrowTable
} from "streamlit-component-lib"

import { VegaLite, SignalListener, VisualizationSpec, PlainObject } from "react-vega";
import { Table } from "apache-arrow"

// import {arrow} from 'vega-loader-arrow';
import {arrow} from './arrow-loader';

interface VegaLiteEventsProps {
  args: {
    spec: VisualizationSpec; // vega lite spec
    data: Table | PlainObject;
    dataframe_key: string; // only used if data is a dataframe
    width: number;
    height: number;
  }
}

function handleSignals(name: string, payload: any) {
  Streamlit.setComponentValue({
    name,
    ...payload
  })
}

const VegaLiteEvents: React.FC<VegaLiteEventsProps> = (props) => {

  const { spec, height, width, data, dataframe_key } = props.args;

  useEffect(() => {
    Streamlit.setFrameHeight(height + 30); // some buffer for axis labels
  }, [height]);

  const signalListeners = useMemo(() => {
    const listenerMap: Record<string, SignalListener> = {};
    // Override typecheck since "selection" is missing from the defintion for VLSpecs
    Object.keys((spec as any).selection).forEach((key: string) => {
      listenerMap[key] = handleSignals
    });
    return listenerMap;
  }, [spec]);


  const dataAsObject = useMemo(() => {
    if (data instanceof ArrowTable) {
      console.log(data.table.length)
      console.log(data.table instanceof Table)
      return {
        [dataframe_key]: arrow(data.table)
      }
    } else {
      return data as PlainObject;
    }
  }, [data, dataframe_key]);

  console.log(dataAsObject);

  return (
      <VegaLite
        data={dataAsObject}
        spec={spec}
        signalListeners={signalListeners}
        width={width}
        height={height}
      />
  )
}



export default withStreamlitConnection(VegaLiteEvents)
