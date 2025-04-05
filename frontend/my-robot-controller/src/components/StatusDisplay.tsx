import React from 'react';
import { RobotStatus, ConnectionStatus } from '../types';
import styles from './StatusDisplay.module.css'; // We'll create this CSS file

interface StatusDisplayProps {
  status: RobotStatus | null;
  connection: ConnectionStatus;
}

const StatusDisplay: React.FC<StatusDisplayProps> = ({ status, connection }) => {
  const getConnectionIndicator = () => {
    switch (connection) {
      case 'connected':
        return <span className={`${styles.indicator} ${styles.connected}`} title="Connected"></span>;
      case 'connecting':
        return <span className={`${styles.indicator} ${styles.connecting}`} title="Connecting..."></span>;
      case 'disconnected':
        return <span className={`${styles.indicator} ${styles.disconnected}`} title="Disconnected"></span>;
      case 'error':
        return <span className={`${styles.indicator} ${styles.error}`} title="Connection Error"></span>;
      default:
        return null;
    }
  };

  return (
    <div className={styles.statusCard}>
      <h2 className={styles.title}>
        Robot Status
        {getConnectionIndicator()}
      </h2>
      {connection === 'connecting' && <p>Connecting to robot stream...</p>}
      {connection === 'disconnected' && <p>Disconnected from robot stream.</p>}
      {connection === 'error' && <p>Error connecting to robot stream.</p>}

      {status && connection === 'connected' ? (
        <div className={styles.statusGrid}>
          <div>State:</div> <div><span className={`${styles.state} ${styles[status.state]}`}>{status.state}</span></div>
          <div>Fan Speed:</div> <div>{status.fan_speed}</div>
          <div>Temperature:</div> <div>{status.temperature} °C</div>
          <div>Uptime:</div> <div>{status.uptime} s</div>

          <div>Power Consumption:</div> <div>{status.power_consumption} W</div>
           <div>Last Update:</div> <div>{new Date(status.timestamp).toLocaleTimeString()}</div>
            <div>Logs:</div>
          <div>
            {status.logs.map((log, index) => (
              <div key={index}>
                <p>{log}</p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        connection === 'connected' && <p>Waiting for status data...</p>
      )}
    </div>
  );
};

export default StatusDisplay;