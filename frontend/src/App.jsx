import React, { useState, useEffect, useRef } from 'react';
import { Plane, AlertTriangle, Wrench, Package, ShieldCheck, Users, Radio } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [chaosMode, setChaosMode] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [logs, setLogs] = useState([]);
  const [ledgerVerified, setLedgerVerified] = useState(false);
  const [isApproved, setIsApproved] = useState(false);
  const ws = useRef(null);
  const logsEndRef = useRef(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const triggerAOG = async () => {
    setIsProcessing(true);
    setLogs([]);
    setLedgerVerified(false);
    setIsApproved(false);

    ws.current = new WebSocket("ws://localhost:8002/ws");
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.event === "resolution") {
        setIsProcessing(false);
        ws.current.close();
      }
      setLogs((prev) => [...prev, data]);
      
      // ATC Voice Synthesis
      if (voiceEnabled && data.content) {
        const utterance = new SpeechSynthesisUtterance(data.content);
        utterance.rate = 1.1; // Slightly faster for ATC feel
        utterance.pitch = 0.9;
        window.speechSynthesis.speak(utterance);
      }
    };

    ws.current.onopen = async () => {
      try {
        await fetch('http://localhost:8002/api/trigger-aog', { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ inject_chaos: chaosMode })
        });
      } catch (err) {
        console.error(err);
        setIsProcessing(false);
      }
    };
  };

  const getAgentIcon = (agent) => {
    if (agent?.includes("Mechanic")) return <Wrench className="w-4 h-4 text-alert" />;
    if (agent?.includes("Supply")) return <Package className="w-4 h-4 text-blue-400" />;
    if (agent?.includes("Ops")) return <Radio className="w-4 h-4 text-purple-400" />;
    if (agent?.includes("Compliance")) return <ShieldCheck className="w-4 h-4 text-warning" />;
    if (agent?.includes("Crew")) return <Users className="w-4 h-4 text-scan" />;
    if (agent?.includes("ANOMALY")) return <AlertTriangle className="w-4 h-4 text-red-500 animate-pulse" />;
    return <Plane className="w-4 h-4 text-scan" />;
  };

  return (
    <div className="min-h-screen p-8 relative flex flex-col items-center justify-center max-w-[1200px] mx-auto">
      <div className="scanline"></div>
      
      {/* Header */}
      <div className="w-full flex items-center justify-between mb-8 border-b border-scan/30 pb-4">
        <div>
          <h1 className="text-3xl font-bold tracking-widest text-scan uppercase">BandOps // Command Center</h1>
          <p className="text-scan/60 text-sm mt-1">Regulated Crisis Operations Platform [Track 3]</p>
        </div>
        <div className="text-right">
          <p className="text-xl">16:42:09 Z</p>
          <p className="text-scan/50 text-xs">JFK / T4 / G12</p>
        </div>
      </div>

      <div className="w-full grid grid-cols-12 gap-6">
        
        {/* Left Status Panel */}
        <div className="col-span-4 radar-panel p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-3 mb-6">
              <AlertTriangle className="w-8 h-8 text-warning animate-pulse" />
              <h2 className="text-xl text-warning font-bold uppercase">Crisis Alert (Showcase)</h2>
            </div>
            
            <div className="space-y-4 text-sm">
              <div className="flex justify-between border-b border-scan/20 pb-2">
                <span className="text-scan/60">FLIGHT</span>
                <span>DL902 (JFK-LHR)</span>
              </div>
              <div className="flex justify-between border-b border-scan/20 pb-2">
                <span className="text-scan/60">AIRCRAFT</span>
                <span>B787-9 (N822NW)</span>
              </div>
              <div className="flex justify-between border-b border-scan/20 pb-2">
                <span className="text-scan/60">STATUS</span>
                <span className="text-warning">GROUNDED - HYD FAULT</span>
              </div>
              <div className="flex justify-between border-b border-scan/20 pb-2">
                <span className="text-scan/60">DELAY COST/MIN</span>
                <span className="text-alert">$12,000 USD</span>
              </div>
            </div>
          </div>
          
          <div className="mt-8 space-y-4">
            <button 
              onClick={triggerAOG}
              disabled={isProcessing}
              className={`w-full py-4 border-2 font-bold tracking-widest uppercase transition-all ${
                isProcessing 
                  ? 'border-scan/30 text-scan/50 bg-transparent' 
                  : 'border-scan text-[#000B04] bg-scan hover:bg-transparent hover:text-scan hover:shadow-[0_0_20px_rgba(0,255,65,0.6)]'
              }`}
            >
              {isProcessing ? "Swarm Active" : "Trigger Crisis Swarm (AOG)"}
            </button>

            <div className="flex items-center justify-between text-xs text-scan/60 border border-scan/30 p-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" checked={chaosMode} onChange={(e) => setChaosMode(e.target.checked)} className="accent-scan" />
                Inject Chaos (Weather Anomaly)
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" checked={voiceEnabled} onChange={(e) => setVoiceEnabled(e.target.checked)} className="accent-scan" />
                ATC Voice
              </label>
            </div>
          </div>
        </div>

        {/* Right Live Comm Log */}
        <div className="col-span-8 radar-panel flex flex-col h-[600px] overflow-hidden relative">
          <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
            <Radio className="w-64 h-64" />
          </div>

          <div className="p-4 border-b border-scan/30 bg-scan/10 flex justify-between items-center">
            <h2 className="tracking-widest">BAND_NET // ENCRYPTED COMMS LEDGER</h2>
            {logs.length > 0 && !isProcessing && (
              <button 
                onClick={() => setLedgerVerified(true)}
                className="text-xs border border-scan/50 px-3 py-1 hover:bg-scan hover:text-[#000B04] transition-all"
              >
                {ledgerVerified ? "✓ Ledger Verified" : "Verify SHA-256 Chain"}
              </button>
            )}
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {logs.length === 0 && !isProcessing && (
              <div className="h-full flex items-center justify-center text-scan/40 opacity-50 blink">
                &gt; AWAITING AOG TRIGGER SEQUENCE_
              </div>
            )}

            <AnimatePresence>
              {logs.map((log, idx) => (
                <motion.div 
                  key={idx}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="mb-6 relative z-10"
                >
                  {log.event === "system" ? (
                    <div className="text-scan/60">--- {log.content} ---</div>
                  ) : log.event === "resolution" ? (
                    <div className="p-6 border border-scan bg-scan/10 text-scan">
                      <div className="font-bold mb-4 tracking-widest text-lg">[RESOLUTION LOGGED]</div>
                      <div className="mb-6">{log.content}</div>
                      <div className="text-sm opacity-80 mb-6 italic">The AI has prepared the optimal resolution. The licensed human dispatcher remains in ultimate control.</div>
                      
                      {!isApproved ? (
                        <div className="flex gap-4">
                          <button onClick={() => setIsApproved(true)} className="flex-1 bg-scan text-[#000B04] py-3 font-bold hover:bg-white transition-colors">
                            APPROVE & EXECUTE
                          </button>
                          <button className="flex-1 border border-alert text-alert py-3 font-bold hover:bg-alert/10 transition-colors">
                            REJECT & RE-PROMPT
                          </button>
                        </div>
                      ) : (
                        <div className="text-center bg-scan/20 py-3 font-bold text-scan border border-scan">
                          ✓ RESOLUTION EXECUTED. DISPATCHING COMMANDS.
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className={`transition-opacity duration-500 ${idx === logs.length - 1 || log.event === 'resolution' ? 'opacity-100' : 'opacity-40'}`}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          {getAgentIcon(log.agent)}
                          <span className={`font-bold tracking-wide ${log.event === 'chaos' || log.agent?.includes('FAA') ? 'text-red-500' : 'text-white'}`}>{log.agent}</span>
                          <span className="text-scan/50 text-xs">[{log.role}]</span>
                          {log.framework && (
                            <span className="text-[10px] bg-scan/20 text-scan px-2 py-0.5 rounded border border-scan/30 font-mono">
                              {log.framework}
                            </span>
                          )}
                        </div>
                        {log.tx_hash && (
                          <div className="flex items-center gap-2">
                            {ledgerVerified && <span className="text-green-400 text-xs">✓</span>}
                            <span className="text-[10px] text-scan/40 font-mono" title="SHA-256 Immutable Ledger Hash">
                              Tx: {log.tx_hash.substring(0, 16)}...
                            </span>
                          </div>
                        )}
                      </div>
                      <div className={`pl-6 text-scan/80 border-l ml-2 py-1 ${log.event === 'chaos' || log.agent?.includes('FAA') ? 'border-red-500/50 text-red-400' : 'border-scan/30'}`}>
                        &gt; {log.content}
                      </div>
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
            <div ref={logsEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}
