import React, {useState} from 'react';
import {RobotStateCommand, RobotStatus} from '../types';
import styles from './ControlPanel.module.css';


const API_BASE = 'http://localhost:8000/api';

async function sendCommand<T>(endpoint: string, data?: T): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: data ? JSON.stringify(data) : undefined,
        });

        if (!response.ok) {
            console.error(`Failed to ${endpoint}: ${response.status} ${response.statusText}`);
            const res = await response.json();
            alert(`Error: ${res.message}`);
            return false;
        }
        console.log(`Command ${endpoint} successful`);
        return true;
    } catch (error) {
        console.error(`Network error during ${endpoint}:`, error);
        alert('Network error. Please check the connection.');
        return false;
    }
}


interface ControlPanelProps {
    currentFanSpeed?: number,
    status?: RobotStatus|null,
}

const ControlPanel: React.FC<ControlPanelProps> = ({currentFanSpeed,  status}) => {
    const [targetFanSpeed, setTargetFanSpeed] = useState<number>(currentFanSpeed ?? 50);
    const [isSubmitting, setIsSubmitting] = useState<Record<string, boolean>>({});


    const handleAction = async (action: () => Promise<boolean>, actionName: string) => {
        setIsSubmitting(prev => ({...prev, [actionName]: true}));
        await action();
        setIsSubmitting(prev => ({...prev, [actionName]: false}));
    }

    const handleSetState = (state: RobotStateCommand) => {
        handleAction(() => sendCommand('/state/', {state}), `setState-${state}`);
    };

    const handleReset = () => {
        handleAction(() => sendCommand('/reset/'), 'reset');
    };

    const handleChangeFanSpeed = () => {
        handleAction(() => sendCommand('/fan_speed/', {fan_mode: "custom", value: targetFanSpeed}), 'changeFanSpeed');
    };
    const handleChangeFanMode = () => {
        handleAction(() => sendCommand('/fan_speed/', {fan_mode: "linear"}), 'changeFanMode');
    };

    return (
        <div className={styles.controlCard}>
            <h2 className={styles.title}>Robot Control</h2>
            <div  className={styles.controlGroup}>
                <label className={styles.label}>Set State:</label>

                <div className={styles.buttonGroup}>
                    {status?.state === 'OFFLINE' &&
                    <button
                        onClick={() => handleSetState('IDLE')}
                        disabled={isSubmitting['setState-idle']}
                        className={`${styles.button} `}
                    >
                        Turn on
                    </button>
                    }
                    {status?.state === 'IDLE' &&
                    <button
                        onClick={() => handleSetState('RUNNING')}
                        disabled={isSubmitting['setState-running']}
                        className={`${styles.button} ${styles.buttonSuccess}`}
                    >
                        Run
                    </button>}
                    {status?.state === 'RUNNING' &&
                    <button
                        onClick={() => handleSetState('IDLE')}
                        disabled={isSubmitting['setState-stopped']}
                        className={`${styles.button} ${styles.buttonWarning}`}
                    >
                        Stop
                    </button>}
                    {(status?.state === 'RUNNING' || status?.state === 'IDLE' ||status?.state === "ERROR") &&
                    <button
                        onClick={() => handleSetState('OFFLINE')}
                        disabled={isSubmitting['setState-stopped']}
                        className={`${styles.button} ${styles.buttonDanger}`}
                    >
                        Turn off
                    </button>}
                </div>
                </div>

            <div className={styles.controlGroup}>
                <label className={styles.label}>Fan Speed ({targetFanSpeed}):</label>
                <div className={styles.fanControl}>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={targetFanSpeed}
                        onChange={(e) => setTargetFanSpeed(parseInt(e.target.value, 10))}
                        className={styles.slider}
                        disabled={isSubmitting['changeFanSpeed']}
                    />

                    <button
                        onClick={handleChangeFanSpeed}
                        disabled={isSubmitting['changeFanSpeed']}
                        className={styles.button}
                    >
                        Set Fan Speed
                    </button>
                    <button
                        onClick={handleChangeFanMode}
                        disabled={isSubmitting['changeFanSpeed']}
                        className={styles.button}
                    >
                        Linear Fan Speed
                    </button>
                </div>
            </div>


            <div className={styles.controlGroup}>
                <label className={styles.label}>Actions:</label>
                <button
                    onClick={handleReset}
                    disabled={isSubmitting['reset']}
                    className={`${styles.button} ${styles.buttonDanger}`}
                >
                    🔄 Reset Robot
                </button>
            </div>
        </div>
    );
};

export default ControlPanel;