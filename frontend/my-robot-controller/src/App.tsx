import  { useState, useEffect, useRef } from 'react';
import { RobotStatus, ConnectionStatus } from './types';
import StatusDisplay from './components/StatusDisplay';
import ControlPanel from './components/ControlPanel.tsx';
import styles from './App.module.css';

const STREAM_URL = import.meta.env.VITE_API_BASE + "/stream" || 'http://localhost:5478/api/stream';

function App() {
  const [robotStatus, setRobotStatus] = useState<RobotStatus | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('connecting');
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    console.log('Setting up EventSource...');
    setConnectionStatus('connecting');

    if (eventSourceRef.current) {
        eventSourceRef.current.close();
        console.log('Closed existing EventSource.');
    }

    const eventSource = new EventSource(STREAM_URL);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      console.log('SSE Connection established');
      setConnectionStatus('connected');
    };

    eventSource.onmessage = (event) => {
      try {
        const data: RobotStatus = JSON.parse(event.data);
        if (!data.timestamp) {
            data.timestamp = new Date().toISOString();
        }
        setRobotStatus(data);
        if (connectionStatus !== 'connected') {
            setConnectionStatus('connected');
        }
      } catch (error) {
        console.error('Failed to parse status update:', event.data, error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      setConnectionStatus('error');

       if (eventSource.readyState === EventSource.CLOSED) {
            console.log("SSE connection closed definitively.");
            setConnectionStatus('disconnected');
            eventSourceRef.current = null;
        } else {
             setConnectionStatus('error');
        }
    };

    return () => {
      if (eventSourceRef.current) {
        console.log('Closing EventSource...');
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    };
  }, []);

  return (
    <div className={styles.appContainer}>
      <header className={styles.header}>
        <h1>🤖 Robot Controller</h1>
      </header>
      <main className={styles.mainContent}>
        <StatusDisplay status={robotStatus} connection={connectionStatus} />
        <ControlPanel status = {robotStatus} currentFanSpeed={robotStatus?.fan_speed} />
      </main>
      <footer className={styles.footer}>
        React Robot Interface v1.0
      </footer>
    </div>
  );
}

export default App;