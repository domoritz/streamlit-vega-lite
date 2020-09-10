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

interface VegaLiteComponentProps {
  args: {
    spec: VisualizationSpecWithDimensions;
    data: Table | PlainObject;
    dataframe_key: string; // only used if data is a dataframe (Table)
  }
}

function handleSignals(name: string, payload: any) {
  Streamlit.setComponentValue({
    name,
    ...payload
  })
}

const VegaLiteComponent: React.FC<VegaLiteComponentProps> = (props) => {
  const { spec, data, dataframe_key } = props.args;
  const { height = 200, width = 200 } = spec;

  useEffect(() => {
    Streamlit.setFrameHeight(height + 30); // magic number buffer for X axis labels
  }, [height]);

  const signalListeners = useMemo(() => {
    const listenerMap: Record<string, SignalListener> = {};
    // Override type since "selection" is missing from the defintion for VisualizationSpec
    Object.keys((spec as any).selection).forEach((key: string) => {
      listenerMap[key] = handleSignals
    });
    return listenerMap;
  }, [spec]);


  const dataAsObject = useMemo(() => {
    if (data instanceof ArrowTable) {
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

export default withStreamlitConnection(VegaLiteComponent)
