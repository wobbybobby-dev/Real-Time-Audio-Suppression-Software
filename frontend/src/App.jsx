import React, { useState, useEffect } from "react";
import { ModeSelector } from "./components/ModeSelector";
import StatusBar from "./components/StatusBar";
import FrequencyVisualiser from "./components/FrequencyVisualiser";
import TargetSpeakerCard from "./components/TargetSpeakerCard";
import { useAudioWS } from "./hooks/useAudioWebSocket";

import "./styles/globals.css";
import "./styles/app.css";

export default function App() {
  const [mode, setMode] = useState("focus_speech");
  const [strength, setStrength] = useState(0.8);

  const { 
    connected, 
    streaming, 
    startStreaming,
    stopStreaming,
    inputSpectrum,
    outputSpectrum,
    updateControl
  } = useAudioWS(mode, strength);


  const handleModeChange = (newMode) => {
    setMode(newMode);
    updateControl(newMode, strength);
    };

  return (
    <div className="app-container">
      
      <header className="header">
        <div>
          <h1 className="title">SOUNDFILTER</h1>
          <p className="subtitle">Selective Audio</p>
        </div>

        <button
          className="start-btn"
          onClick={streaming ? stopStreaming : startStreaming}
        >
          {streaming ? "Stop" : "Start"}
        </button>
      </header>

      <StatusBar connected={connected} streaming={streaming} />

      <div className="main-grid">

        <div className="visualiser-panel">
          <h3>FREQUENCY SPECTRUM</h3>
          <FrequencyVisualiser 
            input={inputSpectrum} 
            output={outputSpectrum} 
          />
        </div>

        <div className="control-panel">

          <h3>Toggle and tune each source</h3>

          <ModeSelector 
            currentMode={mode} 
            onModeChange={handleModeChange} 
          />

          <TargetSpeakerCard
                strength={strength}
                setStrength={(val) => {
                    setStrength(val);
                    updateControl(mode, val);
                }}
            />

        </div>
      </div>
    </div>
  );
}
