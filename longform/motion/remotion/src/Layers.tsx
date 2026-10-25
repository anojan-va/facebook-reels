import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, staticFile, Easing, delayRender, continueRender } from "remotion";

const YELLOW = "#ffd60a";
const RED = "#eb3232";
// Load the channel fonts before the first frame is captured.
const fontHandle = delayRender("fonts");
Promise.all([["Anton", "Anton-Regular.ttf"], ["Mont", "Montserrat-Black.ttf"]].map(([name, file]) =>
  new FontFace(name, `url(${staticFile(file)})`, { weight: "100 900" }).load().then((ff) => { document.fonts.add(ff); })))
  .then(() => continueRender(fontHandle));
const Fonts = () => null;
const anton: React.CSSProperties = { fontFamily: "Anton", textTransform: "uppercase", lineHeight: 1 };
const mont: React.CSSProperties = { fontFamily: "Mont", fontWeight: 800, textTransform: "uppercase", letterSpacing: 6 };
const shadow = "0 6px 30px rgba(0,0,0,0.85), 0 0 4px rgba(0,0,0,0.9)";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const useOut = (frames = 8) => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return interpolate(f, [durationInFrames - frames, durationInFrames], [1, 0], clamp);
};

// Two-line title: top word slams down, bottom line types in letter by letter with a glitch offset.
export const TitleSlam: React.FC<{ top: string; bottom: string }> = ({ top, bottom }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out = useOut();
  const s = spring({ frame: f, fps, config: { damping: 12, stiffness: 220 } });
  const n = Math.floor(interpolate(f, [8, 26], [0, bottom.length], clamp));
  const jitter = f > 8 && f < 28 && f % 3 === 0 ? 6 : 0;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: out }}>
      <Fonts />
      <div style={{ ...anton, fontSize: 230, color: "white", letterSpacing: 10, textShadow: shadow,
        transform: `scale(${interpolate(s, [0, 1], [2.4, 1])})`, opacity: interpolate(f, [0, 3], [0, 1], clamp),
        marginTop: -160 }}>{top}</div>
      <div style={{ ...anton, fontSize: 104, color: YELLOW, letterSpacing: 4, marginTop: 10,
        textShadow: `${shadow}, 0 0 24px rgba(255,214,10,0.55)`, transform: `translateX(${jitter}px)` }}>
        {bottom.slice(0, n)}
      </div>
    </AbsoluteFill>
  );
};

// Number counting up with unit, optional speed dial arc, sub label.
export const BigNumber: React.FC<{ to: number; unit: string; sub?: string; y?: number; decimals?: number; dial?: boolean }> =
  ({ to, unit, sub, y = 0.42, decimals = 0, dial }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out = useOut();
  const k = interpolate(f, [2, 30], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const done = f >= 30;
  const pop = done ? 1 + 0.12 * Math.exp(-(f - 30) / 4) : 1;
  const enter = spring({ frame: f, fps, config: { damping: 14, stiffness: 200 } });
  const R = 380, C = Math.PI * R * 1.5;
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <Fonts />
      {dial && (
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <g transform={`translate(960 ${y * 1080 + 10}) rotate(135)`} opacity={interpolate(f, [0, 6], [0, 1], clamp)}>
            <circle r={R} fill="none" stroke="rgba(255,255,255,0.18)" strokeWidth={26} strokeDasharray={`${C} 9999`} />
            <circle r={R} fill="none" stroke={YELLOW} strokeWidth={26} strokeDasharray={`${C * k} 9999`}
              style={{ filter: "drop-shadow(0 0 14px rgba(255,214,10,0.8))" }} />
            {Array.from({ length: 13 }).map((_, i) => {
              const a = (i / 12) * 270 * Math.PI / 180;
              return <line key={i} x1={Math.cos(a) * (R - 40)} y1={Math.sin(a) * (R - 40)} x2={Math.cos(a) * (R - 70)}
                y2={Math.sin(a) * (R - 70)} stroke="white" strokeWidth={5} opacity={0.7} />;
            })}
          </g>
        </svg>
      )}
      <div style={{ position: "absolute", top: y * 1080 - 150, width: 1920, textAlign: "center",
        transform: `scale(${interpolate(enter, [0, 1], [0.6, 1]) * pop})` }}>
        <span style={{ ...anton, fontSize: 230, color: done ? YELLOW : "white", textShadow: `${shadow}${done ? ", 0 0 40px rgba(255,214,10,0.6)" : ""}` }}>
          {(to * k).toFixed(decimals)}
        </span>
        <span style={{ ...anton, fontSize: 90, color: "white", marginLeft: 18, textShadow: shadow }}>{unit}</span>
      </div>
      {sub && (
        <div style={{ ...mont, position: "absolute", top: y * 1080 + 120, width: 1920, textAlign: "center", fontSize: 40,
          color: "white", textShadow: shadow, opacity: interpolate(f, [22, 32], [0, 1], clamp),
          transform: `translateY(${interpolate(f, [22, 32], [20, 0], clamp)}px)` }}>{sub}</div>
      )}
    </AbsoluteFill>
  );
};

// HUD countdown "T-MINUS hh:mm:ss" ticking down in real seconds x rate, with a blinking red rec dot and frame brackets.
export const Countdown: React.FC<{ from: number; label: string; rate?: number }> = ({ from, label, rate = 1 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out = useOut();
  const left = Math.max(0, Math.ceil(from - (f / fps) * rate));
  const hh = String(Math.floor(left / 3600)).padStart(2, "0");
  const mm = String(Math.floor((left % 3600) / 60)).padStart(2, "0");
  const ss = String(left % 60).padStart(2, "0");
  const enter = spring({ frame: f, fps, config: { damping: 15, stiffness: 180 } });
  const blink = Math.floor(f / 8) % 2 === 0;
  const b = 60, L = 90;
  const corner = (x: number, y: number, sx: number, sy: number) => (
    <path d={`M ${x + sx * L} ${y} L ${x} ${y} L ${x} ${y + sy * L}`} stroke="white" strokeWidth={6} fill="none" opacity={0.85} />
  );
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <Fonts />
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: enter }}>
        {corner(b, b, 1, 1)}{corner(1920 - b, b, -1, 1)}{corner(b, 1080 - b, 1, -1)}{corner(1920 - b, 1080 - b, -1, -1)}
      </svg>
      <div style={{ position: "absolute", left: 110, top: 100, display: "flex", alignItems: "center", gap: 18, opacity: enter }}>
        <div style={{ width: 30, height: 30, borderRadius: 15, background: RED, opacity: blink ? 1 : 0.15,
          boxShadow: `0 0 20px ${RED}` }} />
        <div style={{ ...mont, fontSize: 40, color: "white", textShadow: shadow }}>{label}</div>
      </div>
      <div style={{ position: "absolute", top: 330, width: 1920, textAlign: "center",
        transform: `scale(${interpolate(enter, [0, 1], [1.6, 1])})` }}>
        <div style={{ ...mont, fontSize: 52, color: RED, letterSpacing: 18, textShadow: shadow }}>T-MINUS</div>
        <div style={{ ...anton, fontSize: 250, color: "white", letterSpacing: 8, fontVariantNumeric: "tabular-nums",
          textShadow: `${shadow}, 0 0 30px rgba(235,50,50,0.5)` }}>{hh}:{mm}:{ss}</div>
      </div>
    </AbsoluteFill>
  );
};

// Red rubber stamp slamming in at an angle, sub line under it.
export const Stamp: React.FC<{ text: string; sub?: string }> = ({ text, sub }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out = useOut();
  const s = spring({ frame: f, fps, config: { damping: 9, stiffness: 260 } });
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: out }}>
      <Fonts />
      <div style={{ transform: `rotate(-7deg) scale(${interpolate(s, [0, 1], [3, 1])})`, opacity: interpolate(f, [0, 3], [0, 1], clamp),
        border: `12px solid ${RED}`, padding: "18px 50px", borderRadius: 14, marginTop: -120,
        background: "rgba(0,0,0,0.35)", boxShadow: `0 0 40px rgba(235,50,50,0.5)` }}>
        <div style={{ ...anton, fontSize: 150, color: RED, letterSpacing: 6 }}>{text}</div>
      </div>
      {sub && <div style={{ ...mont, fontSize: 42, color: "white", marginTop: 40, textShadow: shadow,
        opacity: interpolate(f, [12, 20], [0, 1], clamp) }}>{sub}</div>}
    </AbsoluteFill>
  );
};

// Targeting reticle locking onto a point, coordinates scrambling, then a label/value.
export const Reticle: React.FC<{ label: string; value: string; x?: number; y?: number }> = ({ label, value, x = 0.5, y = 0.45 }) => {
  const f = useCurrentFrame();
  const out = useOut();
  const cx = x * 1920, cy = y * 1080;
  const k = interpolate(f, [0, 18], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.6)) });
  const r = interpolate(k, [0, 1], [520, 170]);
  const rot = interpolate(f, [0, 75], [-60, 30]);
  const rnd = (i: number) => Math.abs(Math.sin(f * 12.9898 + i * 78.233) * 43758.5453) % 1;
  const lat = f < 40 ? (rnd(1) * 90).toFixed(2) : "??.??";
  const lon = f < 40 ? (rnd(2) * 180).toFixed(2) : "???.??";
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <Fonts />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <g transform={`translate(${cx} ${cy}) rotate(${rot})`} opacity={interpolate(f, [0, 5], [0, 1], clamp)}
          style={{ filter: "drop-shadow(0 0 10px rgba(235,50,50,0.9))" }}>
          <circle r={r} fill="none" stroke={RED} strokeWidth={6} strokeDasharray="40 22" />
          <circle r={r * 0.55} fill="none" stroke={RED} strokeWidth={4} />
          {[0, 90, 180, 270].map((a) => (
            <line key={a} x1={0} y1={r * 0.7} x2={0} y2={r * 1.3} stroke={RED} strokeWidth={6} transform={`rotate(${a})`} />
          ))}
        </g>
        <circle cx={cx} cy={cy} r={8} fill={RED} opacity={Math.floor(f / 5) % 2 ? 1 : 0.3} />
      </svg>
      <div style={{ ...mont, position: "absolute", left: cx + 270, top: cy - 120, fontSize: 30, color: "white", textShadow: shadow,
        opacity: interpolate(f, [10, 16], [0, 1], clamp), lineHeight: 1.5 }}>
        LAT {lat}°<br />LON {lon}°
      </div>
      <div style={{ position: "absolute", left: cx + 270, top: cy - 10, opacity: interpolate(f, [24, 30], [0, 1], clamp) }}>
        <div style={{ ...mont, fontSize: 34, color: RED, textShadow: shadow }}>{label}</div>
        <div style={{ ...anton, fontSize: 120, color: "white", textShadow: shadow,
          transform: `scale(${interpolate(f, [40, 46], [1.3, 1], clamp)})`, transformOrigin: "left" }}>{f < 40 ? "SCANNING" : value}</div>
      </div>
    </AbsoluteFill>
  );
};

// Lower-left callout with a sliding yellow bar, title and typed sub line.
export const Callout: React.FC<{ title: string; sub: string }> = ({ title, sub }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out = useOut(10);
  const s = spring({ frame: f, fps, config: { damping: 16, stiffness: 170 } });
  const n = Math.floor(interpolate(f, [10, 36], [0, sub.length], clamp));
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <Fonts />
      <div style={{ position: "absolute", left: 110, top: 560, transform: `translateX(${interpolate(s, [0, 1], [-900, 0])}px)`,
        display: "flex" }}>
        <div style={{ width: 14, background: YELLOW, boxShadow: `0 0 18px ${YELLOW}` }} />
        <div style={{ background: "rgba(0,0,0,0.62)", padding: "20px 36px 24px" }}>
          <div style={{ ...anton, fontSize: 84, color: "white", letterSpacing: 3 }}>{title}</div>
          <div style={{ ...mont, fontSize: 30, color: YELLOW, marginTop: 10, minHeight: 36, letterSpacing: 3 }}>{sub.slice(0, n)}</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
