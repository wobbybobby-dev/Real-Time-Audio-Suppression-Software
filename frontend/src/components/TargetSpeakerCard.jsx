import React from 'react';

export default function TargetSpeakerCard({
  strength,
  setStrength,
  startStreaming,
  streaming
}) {
  return (
    <section className="panel">
      
      {/* Strength slider */}
      <div style={{ marginBottom: "1.5rem" }}>
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: "0.7rem",
          color: "#94a3b8",
          marginBottom: "0.4rem"
        }}>
          <span>SUPPRESSION</span>
          <span style={{ color: "#00f2ff" }}>
            {(strength * 100).toFixed(0)}%
          </span>
        </div>

        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={strength}
          onChange={(e) => setStrength(parseFloat(e.target.value))}
          style={{
            width: "100%",
            accentColor: "#00f2ff"
          }}
        />
      </div>

    </section>
  );
}
