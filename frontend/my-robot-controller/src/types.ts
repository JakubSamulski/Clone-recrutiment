export interface RobotStatus {
  state: 'IDLE' | 'RUNNING' | 'OFFLINE' | 'ERROR';
  temperature: number;
  fan_speed: number;
  power_consumption: string;
  uptime: string ;
  timestamp: string;
  logs: string[];
}

export type RobotStateCommand = 'RUNNING' | 'IDLE' | 'OFFLINE';

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';