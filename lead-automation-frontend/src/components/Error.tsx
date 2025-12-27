interface ErrorProps {
    message: string;
    onRetry?: () => void;
}

export default function Error({ message, onRetry }: ErrorProps) {
    return (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <div className="text-red-600 text-4xl mb-4">⚠️</div>
            <p className="text-red-800 mb-4">{message}</p>
            {onRetry && (
                <button
                    onClick={onRetry}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                    Retry
                </button>
            )}
        </div>
    );
}
