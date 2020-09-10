import React, { ReactNode } from "react";
import { SignalListener, VegaLite, View } from "react-vega";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import {arrow} from './arrow-loader';


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
    console.log(this.props)
    const {spec, ...args} = this.props.args;

    if (spec.selection) {
      for (const selectionName of Object.keys(spec.selection)) {
        this.signalListeners[selectionName] = this.handleSignals
      }
    }

    const data: Record<string, any> = {};
    for (const name of Object.keys(args ?? {})) {
      data[name] = arrow(args[name].table);
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
