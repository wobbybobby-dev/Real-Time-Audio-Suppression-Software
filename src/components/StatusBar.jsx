import React from 'react';

export default function StatusBar({ connected, streaming }) {
  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: "1rem"
    }}>
      {/* Connection Status */}
      <div className={`status-pill ${connected ? 'active' : ''}`}>
        {connected ? 'Engine Ready' : 'Connecting...'}
      </div>

      {/* Streaming State */}
      <div style={{
        fontSize: "0.7rem",
        color: "#94a3b8",
        letterSpacing: "1px",
        textTransform: "uppercase"
      }}>
        {streaming ? "Live Processing" : "Idle"}
      </div>
    </div>
  );
}