import { User, Construction, VolumeX, Mic } from 'lucide-react';

const SCENARIOS = [
  { 
    id: 'focus_speech', 
    label: 'Scenario 1 & 2: Focus Speech', 
    desc: 'Isolate friends/family, block environment.',
    icon: <User size={20} /> 
  },
  { 
    id: 'block_speech', 
    label: 'Scenario 3: Block Voices', 
    desc: 'Keep TV/Fans, block chatter.',
    icon: <VolumeX size={20} /> 
  },
  { 
    id: 'construction_block', 
    label: 'Extreme Construction', 
    desc: 'Aggressive sub-band filtering.',
    icon: <Construction size={20} /> 
  }
];

export function ModeSelector({ currentMode, onModeChange }) {
  return (
    <div className="mode-grid">
      {SCENARIOS.map((s) => (
        <button 
          key={s.id}
          className={`mode-card ${currentMode === s.id ? 'active' : ''}`}
          onClick={() => onModeChange(s.id)}
        >
          <div className="icon-circle">{s.icon}</div>
          <div className="mode-info">
            <span className="mode-label">{s.label}</span>
            <span className="mode-desc">{s.desc}</span>
          </div>
        </button>
      ))}
    </div>
  );
}