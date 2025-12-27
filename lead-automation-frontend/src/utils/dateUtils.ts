/**
 * Format date/time in IST timezone
 * Converts UTC time to IST (UTC + 5:30)
 */
export const formatIST = (dateString: string | null | undefined): string => {
    if (!dateString) return 'N/A';

    try {
        const date = new Date(dateString);

        // Convert to IST by adding 5 hours and 30 minutes
        const istDate = new Date(date.getTime() + (5.5 * 60 * 60 * 1000));

        return istDate.toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        }) + ' IST';
    } catch (error) {
        return 'Invalid Date';
    }
};

/**
 * Format date only in IST
 * Converts UTC date to IST (UTC + 5:30)
 */
export const formatDateIST = (dateString: string | null | undefined): string => {
    if (!dateString) return 'N/A';

    try {
        const date = new Date(dateString);

        // Convert to IST by adding 5 hours and 30 minutes
        const istDate = new Date(date.getTime() + (5.5 * 60 * 60 * 1000));

        return istDate.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    } catch (error) {
        return 'Invalid Date';
    }
};

/**
 * Get current time in IST as ISO string for API requests
 */
export const getCurrentISTTime = (): string => {
    const now = new Date();
    // Add 5 hours and 30 minutes to get IST
    const istTime = new Date(now.getTime() + (5.5 * 60 * 60 * 1000));
    return istTime.toISOString();
};

/**
 * Convert IST time to UTC for API requests
 */
export const convertISTtoUTC = (istDate: Date): Date => {
    // Subtract 5 hours and 30 minutes to get UTC
    return new Date(istDate.getTime() - (5.5 * 60 * 60 * 1000));
};
