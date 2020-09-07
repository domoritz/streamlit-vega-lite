import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "./streamlit"

import { VegaLite, SignalListener, View } from "react-vega";

const CHART_HEIGHT = 400;
const CHART_WIDTH = 400;

function handleNewView(view: View) {
  console.log(view);
  // Is there something in here that can be used to help with resolving selectionId to data values?
}

class VegaLiteEvents extends StreamlitComponentBase<{}> {
  public state = { numClicks: 0 }

  // Signal listener type could probably be more specific: single, multi, or interval (brush)
  private signalListeners: Record<string, SignalListener> = {}

  public componentDidMount() {
    Streamlit.setFrameHeight(CHART_HEIGHT + 30); // some buffer for axis labels
  }

  private handleSignals(name: string, payload: any) {
    // if (payload['_vgsid_']) { // single and multi selection
    //   // Need to resolve selections using the data values
    // can't just use as row id in data, as it may not be clear which column the selection applied to
    // In an MVP we could do a lookup in the spec key, but things may break down with multiple encodings.
    // } else { // interval selection returns raw data values

    // }

    Streamlit.setComponentValue({
      name,
      ...payload
    })
  }

  public render = (): ReactNode => {
    const spec = this.props.args["spec"] || {};

    // TODO: add support for processing dataframes directly
    // Need arrow -> object conversion function
    const data = this.props.args["data"] || {};

    if (spec.selection) {
      Object.keys(spec.selection).forEach((key: string) => {
        this.signalListeners[key] = this.handleSignals
      })
    }

    return (
      <div>
        <VegaLite
          data={data}
          spec={spec}
          signalListeners={this.signalListeners}
          width={CHART_WIDTH}
          height={CHART_HEIGHT}
          onNewView={handleNewView}
        />
      </div>
    )
  }
}

export default withStreamlitConnection(VegaLiteEvents)
