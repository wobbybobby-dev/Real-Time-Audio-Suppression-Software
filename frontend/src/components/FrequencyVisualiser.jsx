import React, { useEffect, useRef } from 'react';

export default function FrequencyVisualiser({ input = [], output = [] }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !input.length) return;

    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    //  Reduce bars (important)
    const maxBars = 64;
    const step = Math.floor(input.length / maxBars);
    const bars = maxBars;

    const barWidth = width / bars;

    //  Normalize
    const maxVal = Math.max(...input, ...output, 1e-6);

    for (let i = 0; i < bars; i++) {
      const idx = i * step;

      const inVal = input[idx] / maxVal;
      const outVal = output[idx] / maxVal;

      const inHeight = inVal * height;
      const outHeight = outVal * height;

      // INPUT (background)
      ctx.fillStyle = "rgba(255,255,255,0.15)";
      ctx.fillRect(
        i * barWidth,
        height - inHeight,
        barWidth - 2,
        inHeight
      );

      // OUTPUT (foreground)
      ctx.fillStyle = "#00f2ff";
      ctx.fillRect(
        i * barWidth,
        height - outHeight,
        barWidth - 2,
        outHeight
      );
    }

  }, [input, output]);

  return (
    <canvas
      ref={canvasRef}
      width={600}
      height={200}
      style={{
        width: "100%",
        borderRadius: "12px",
        background: "rgba(0,0,0,0.3)"
      }}
    />
  );
}
