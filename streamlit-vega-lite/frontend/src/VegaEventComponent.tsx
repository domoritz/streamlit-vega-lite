import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "./streamlit"

import { VegaLite, SignalListener } from "react-vega";

const CHART_HEIGHT = 400;
const CHART_WIDTH = 400;

function handleSignals(name: string, payload: any) {
  // console.log(args); // Inverse engeneering
  Streamlit.setComponentValue({
    name,
    ...payload
  })
}

class VegaLiteEvents extends StreamlitComponentBase<{}> {
  public state = { numClicks: 0 }

  // Signal listener type could probably be more specific: single, multi, or interval
  private signalListeners: Record<string, SignalListener> = {
    "highlight": handleSignals,
    "select": handleSignals
  }

  public componentDidMount() {
    Streamlit.setFrameHeight(CHART_HEIGHT + 30); // some buffer for margin
  }

  public render = (): ReactNode => {
    const spec = this.props.args["spec"] || {};

    // TODO: add support for processing dataframes directly
    // Need arrow -> object conversion function
    const data = this.props.args["data"] || {};

    if (spec.selection) {
      Object.keys(spec.selection).forEach((key: string) => {
        this.signalListeners[key] = handleSignals

      })
    }


    return (
      <div>
        <VegaLite spec={spec}
                  signalListeners={this.signalListeners}
                  data={data}
                  width={CHART_WIDTH}
                  height={CHART_HEIGHT}
                  />
      </div>
    )
  }
}

export default withStreamlitConnection(VegaLiteEvents)
