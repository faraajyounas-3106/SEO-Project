import { useEffect, useState } from 'react';

export function useAudit(taskId: string | null, onComplete?: () => void) {
  const [status, setStatus] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) {
      setStatus(null);
      setProgress(0);
      setError(null);
      return;
    }

    setStatus('queued');
    setProgress(0);
    setError(null);

    let intervalId: any;

    const checkStatus = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/audits/${taskId}/status`);
        if (!res.ok) {
          throw new Error('Failed to fetch status');
        }
        const data = await res.json();
        setStatus(data.status);
        setProgress(data.progress_percentage || 0);

        if (data.status === 'completed') {
          clearInterval(intervalId);
          if (onComplete) onComplete();
        } else if (data.status === 'failed') {
          clearInterval(intervalId);
          setError(data.error_message || 'Task failed');
        }
      } catch (err: any) {
        setError(err.message || 'Error parsing status');
        clearInterval(intervalId);
      }
    };

    // Run check status immediately and then poll every 3 seconds
    checkStatus();
    intervalId = setInterval(checkStatus, 3000);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [taskId]);

  return { status, progress, error };
}
