import React, { useMemo } from "react";
import { SignalListener, VegaLite, View } from "react-vega";
import {
  ArrowTable, Streamlit,
  withStreamlitConnection
} from "streamlit-component-lib";
import { TopLevelSpec } from "vega-lite";
import { arrow } from './arrow-loader';

interface Args {
    spec: TopLevelSpec,
    [name: string]: any
}

interface VegaLiteComponentProps {
  args: Args
}

function handleSignals(name: string, payload: any) {
  Streamlit.setComponentValue({
    name,
    ...payload
  })
}

function handleNewView(view: View) {
  view.addResizeListener((_, height) => {
    Streamlit.setFrameHeight(height);
  });
}

const VegaLiteComponent: React.FC<VegaLiteComponentProps> = (props) => {
  const {spec, ...args} = props.args;

  const signalListeners = useMemo(() => {
    const listenerMap: Record<string, SignalListener> = {};

    if ('selection' in spec) {
      for (const selectionName of Object.keys(spec.selection!)) {
        listenerMap[selectionName] = handleSignals
      }
    }

    return listenerMap;
  }, [spec]);

  const data = useMemo(() => {
    const data: Record<string, any> = {};
    for (const name of Object.keys(args ?? {})) {
      const table = args[name];
      data[name] = table instanceof ArrowTable ? arrow(table.table) : table;
    }

    return data;
  }, [args]);

  return (
    <VegaLite
      data={data}
      spec={spec}
      signalListeners={signalListeners}
      onNewView={handleNewView}
    />
  )
}

export default withStreamlitConnection(VegaLiteComponent)
