// Transparent overlay layers for the long-form renderer (rendered as PNG sequences with alpha, composited by
// make_long.py's "clip" overlay). One <Composition> per layer; props come from --props.
import React from "react";
import { Composition } from "remotion";
import { BigNumber, Countdown, Stamp, Reticle, Callout, TitleSlam } from "./Layers";

const base = { fps: 30, width: 1920, height: 1080 };
export const Root: React.FC = () => (
  <>
    <Composition id="TitleSlam" component={TitleSlam} durationInFrames={75} {...base}
      defaultProps={{ top: "WHAT IF", bottom: "AN ASTEROID HIT EARTH?" }} />
    <Composition id="BigNumber" component={BigNumber} durationInFrames={90} {...base}
      defaultProps={{ to: 20, unit: "KM/S", sub: "≈ 72,000 KM/H", y: 0.42, decimals: 0, dial: true }} />
    <Composition id="Countdown" component={Countdown} durationInFrames={90} {...base}
      defaultProps={{ from: 86400, label: "TIME TO IMPACT", rate: 1 }} />
    <Composition id="Stamp" component={Stamp} durationInFrames={60} {...base}
      defaultProps={{ text: "NO TIME TO DEFLECT", sub: "LAUNCH ABORTED" }} />
    <Composition id="Reticle" component={Reticle} durationInFrames={75} {...base}
      defaultProps={{ label: "IMPACT ZONE", value: "UNKNOWN", x: 0.5, y: 0.45 }} />
    <Composition id="Callout" component={Callout} durationInFrames={120} {...base}
      defaultProps={{ title: "NASA DART · 2022", sub: "A SPACECRAFT RAMMED AN ASTEROID ON PURPOSE" }} />
  </>
);
