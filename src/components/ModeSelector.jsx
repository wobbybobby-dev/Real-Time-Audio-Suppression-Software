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
  
];

export function ModeSelector({ currentMode, onModeChange }) {
  return (
    <div className="mode-grid">
        <button onClick={() => onModeChange("focus_speech")}>
             Focus Speech (remove noise)
        </button>

        <button onClick={() => onModeChange("block_speech")}>
             Remove Speech (keep environment)
        </button>
    </div>
  );
}
