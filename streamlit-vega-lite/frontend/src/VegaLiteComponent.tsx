import React, { ReactNode } from "react";
import { SignalListener, VegaLite, View } from "react-vega";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";


class VegaLiteComponent extends StreamlitComponentBase<{}> {
  // Signal listener type could probably be more specific: single, multi, or interval (brush)
  private signalListeners: Record<string, SignalListener> = {}

  public componentDidMount() {
    Streamlit.setFrameHeight(100);
  }

  public handleNewView(view: View) {
    view.addResizeListener((_, height) => {
      Streamlit.setFrameHeight(height);
    });
  }

  private handleSignals(name: string, payload: any) {
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
      Object.keys(spec.selection).forEach((selectionName: string) => {
        this.signalListeners[selectionName] = this.handleSignals
      })
    }

    return (
      <div>
        <VegaLite
          data={data}
          spec={spec}
          signalListeners={this.signalListeners}
          onNewView={this.handleNewView}
        />
      </div>
    )
  }
}

export default withStreamlitConnection(VegaLiteComponent)
