import React, { useEffect, useMemo } from "react"
import {
  withStreamlitConnection,
  Streamlit,
  ArrowTable
} from "streamlit-component-lib"

import { VegaLite, SignalListener, VisualizationSpec, PlainObject } from "react-vega";
import { Table } from "apache-arrow"

import { arrow } from './arrow-loader';

type VisualizationSpecWithDimensions = VisualizationSpec & {
  height?: number;
  width?: number;
}

interface VegaLiteEventsProps {
  args: {
    spec: VisualizationSpecWithDimensions;
    data: Table | PlainObject;
    dataframe_key: string; // only used if data is a dataframe
  }
}

function handleSignals(name: string, payload: any) {
  Streamlit.setComponentValue({
    name,
    ...payload
  })
}

const VegaLiteEvents: React.FC<VegaLiteEventsProps> = (props) => {

  const { spec, data, dataframe_key } = props.args;
  const { height = 200, width = 200 } = spec;

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
