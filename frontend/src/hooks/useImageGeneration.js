import { useState, useEffect, useRef } from 'react';

// Replace hardcoded localhost with the dynamic hostname of the current window
// This allows the app to be accessed from other devices via the VM's IP address.
// Use the current page protocol (http/https) to avoid mixed‑content errors in production.
const defaultUrl = `${window.location.protocol}//${window.location.hostname}:8001`;
let envUrl = import.meta.env.VITE_API_URL;
if (envUrl && (envUrl.includes('localhost') || envUrl.includes('127.0.0.1'))) {
    envUrl = envUrl.replace(/localhost|127\.0\.0\.1/g, window.location.hostname);
}
const API_URL = envUrl || defaultUrl;
export default function useImageGeneration() {
    const [taskId, setTaskId] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, starting, processing, completed, failed
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const pollInterval = useRef(null);

    const generateImage = async (prompt) => {
        setLoading(true);
        setError(null);
        setResult(null);
        setStatus('starting');

        try {
            const response = await fetch(`${API_URL}/api/v1/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();
            if (response.ok) {
                setTaskId(data.task_id);
                setStatus('processing');
            } else {
                throw new Error(data.detail || 'Failed to start generation');
            }
        } catch (err) {
            setError(err.message);
            setLoading(false);
            setStatus('failed');
        }
    };

    useEffect(() => {
        let intervalId;
        if (taskId && (status === 'processing' || status === 'starting')) {
            intervalId = setInterval(async () => {
                try {
                    const response = await fetch(`${API_URL}/api/v1/status/${taskId}`);
                    const data = await response.json();

                    if (response.ok) {
                        if (data.status === 'completed') {
                            setResult(data);
                            setStatus('completed');
                            setLoading(false);
                            clearInterval(intervalId);
                        } else if (data.status === 'failed') {
                            setError(data.error || 'Generation failed');
                            setStatus('failed');
                            setLoading(false);
                            clearInterval(intervalId);
                        }
                    }
                } catch (err) {
                    console.error("Polling error", err);
                }
            }, 2000);
        }
        return () => clearInterval(intervalId);
    }, [taskId, status]);

    return { generateImage, status, result, error, loading };
}
