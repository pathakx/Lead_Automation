import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Phone, Mail, Building2, Calendar, CheckCircle, Clock, AlertTriangle, TrendingUp, Activity, BellOff } from 'lucide-react';
import { formatIST, formatDateIST } from '../utils/dateUtils';

interface FollowUp {
    id: string;
    lead_id: string;
    lead_name: string;
    lead_email: string;
    lead_phone: string;
    lead_company: string;
    lead_role: string;
    lead_status: string;
    message: string;
    scheduled_for: string;
    action: string;
    reason: string;
    products: string[];
    created_at: string;
    metadata: any;
    status: string;
}

interface Stats {
    pending: number;
    completed: number;
    snoozed: number;
    high: number;
    medium: number;
    low: number;
    total: number;
}

export default function FollowUpQueue() {
    const [allFollowUps, setAllFollowUps] = useState<FollowUp[]>([]);
    const [filteredFollowUps, setFilteredFollowUps] = useState<FollowUp[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<'pending' | 'completed' | 'snoozed' | 'high' | 'medium' | 'low'>('pending');
    const [stats, setStats] = useState<Stats>({ pending: 0, completed: 0, snoozed: 0, high: 0, medium: 0, low: 0, total: 0 });

    useEffect(() => {
        fetchData();
        // Refresh every 30 seconds
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, [filter]);

    const fetchData = async () => {
        try {
            // Fetch stats
            const statsResponse = await api.get('/api/follow-ups/stats');
            setStats(statsResponse.data);

            // Fetch follow-ups based on filter
            let endpoint = '/api/follow-ups/pending';
            if (filter === 'completed') {
                endpoint = '/api/follow-ups/completed';
            } else if (filter === 'snoozed') {
                endpoint = '/api/follow-ups/snoozed';
            }

            const response = await api.get(endpoint);
            let data = response.data;

            // Filter by priority if needed
            if (['high', 'medium', 'low'].includes(filter)) {
                data = data.filter((fu: FollowUp) => fu.metadata?.priority === filter);
            }

            setAllFollowUps(response.data);
            setFilteredFollowUps(data);
        } catch (error) {
            console.error('Failed to fetch follow-ups:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleComplete = async (id: string) => {
        const notes = prompt('Enter completion notes (optional):');
        try {
            await api.post(`/api/follow-ups/${id}/complete`, { notes });
            fetchData(); // Refresh data
        } catch (error) {
            console.error('Failed to complete follow-up:', error);
            alert('Failed to mark as completed');
        }
    };

    const handleSnooze = async (id: string) => {
        const hours = prompt('Snooze for how many hours?', '2');
        if (!hours) return;

        const snoozeUntil = new Date();
        snoozeUntil.setHours(snoozeUntil.getHours() + parseInt(hours));

        try {
            await api.post(`/api/follow-ups/${id}/snooze`, {
                snooze_until: snoozeUntil.toISOString()
            });
            fetchData(); // Refresh data
        } catch (error) {
            console.error('Failed to snooze follow-up:', error);
            alert('Failed to snooze');
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'high':
                return 'bg-red-100 text-red-800';
            case 'medium':
                return 'bg-yellow-100 text-yellow-800';
            case 'low':
                return 'bg-green-100 text-green-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    if (loading) {
        return <div className="text-center py-8">Loading follow-ups...</div>;
    }

    return (
        <div className="flex gap-4">
            {/* Left Sidebar - Status Cards */}
            <div className="w-64 flex-shrink-0 space-y-4">
                {/* Completed Card */}
                <button
                    onClick={() => setFilter('completed')}
                    className={`w-full p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'completed' ? 'bg-green-50 border-2 border-green-400' : 'bg-white border-2 border-transparent'
                        }`}
                >
                    <div className="flex flex-col">
                        <div className="flex items-center justify-between mb-2">
                            <CheckCircle className="w-10 h-10 text-green-500" />
                            <span className="text-3xl font-bold text-green-600">{stats.completed}</span>
                        </div>
                        <p className="text-sm font-medium text-gray-700">Completed Tasks</p>
                    </div>
                </button>

                {/* Snoozed Card */}
                <button
                    onClick={() => setFilter('snoozed')}
                    className={`w-full p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'snoozed' ? 'bg-purple-50 border-2 border-purple-400' : 'bg-white border-2 border-transparent'
                        }`}
                >
                    <div className="flex flex-col">
                        <div className="flex items-center justify-between mb-2">
                            <BellOff className="w-10 h-10 text-purple-500" />
                            <span className="text-3xl font-bold text-purple-600">{stats.snoozed}</span>
                        </div>
                        <p className="text-sm font-medium text-gray-700">Snoozed Tasks</p>
                    </div>
                </button>
            </div>

            {/* Main Content */}
            <div className="flex-1 space-y-4">
                {/* Priority Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {/* Pending Card */}
                    <button
                        onClick={() => setFilter('pending')}
                        className={`p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'pending' ? 'bg-blue-50 border-2 border-blue-400' : 'bg-white border-2 border-transparent'
                            }`}
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">Pending</p>
                                <p className="text-3xl font-bold text-blue-600 mt-2">{stats.pending}</p>
                            </div>
                            <Activity className="w-12 h-12 text-blue-400" />
                        </div>
                    </button>

                    {/* High Priority Card */}
                    <button
                        onClick={() => setFilter('high')}
                        className={`p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'high' ? 'bg-red-50 border-2 border-red-400' : 'bg-white border-2 border-transparent'
                            }`}
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">High Priority</p>
                                <p className="text-3xl font-bold text-red-600 mt-2">{stats.high}</p>
                            </div>
                            <AlertTriangle className="w-12 h-12 text-red-400" />
                        </div>
                    </button>

                    {/* Medium Priority Card */}
                    <button
                        onClick={() => setFilter('medium')}
                        className={`p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'medium' ? 'bg-yellow-50 border-2 border-yellow-400' : 'bg-white border-2 border-transparent'
                            }`}
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">Medium</p>
                                <p className="text-3xl font-bold text-yellow-600 mt-2">{stats.medium}</p>
                            </div>
                            <TrendingUp className="w-12 h-12 text-yellow-400" />
                        </div>
                    </button>

                    {/* Low Priority Card */}
                    <button
                        onClick={() => setFilter('low')}
                        className={`p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'low' ? 'bg-green-50 border-2 border-green-400' : 'bg-white border-2 border-transparent'
                            }`}
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">Low Priority</p>
                                <p className="text-3xl font-bold text-green-600 mt-2">{stats.low}</p>
                            </div>
                            <CheckCircle className="w-12 h-12 text-green-400" />
                        </div>
                    </button>
                </div>

                {/* Header */}
                <div className="bg-white rounded-lg shadow p-6 border-b border-gray-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 capitalize">
                                {filter === 'pending' ? 'Pending' :
                                    filter === 'completed' ? 'Completed' :
                                        filter === 'snoozed' ? 'Snoozed' :
                                            filter + ' Priority'} Follow-ups
                            </h2>
                            <p className="text-gray-600 mt-1">
                                {filteredFollowUps.length} follow-up{filteredFollowUps.length !== 1 ? 's' : ''}
                            </p>
                        </div>
                        <button
                            onClick={fetchData}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                        >
                            🔄 Refresh
                        </button>
                    </div>
                </div>

                {/* Follow-up Cards */}
                <div className="space-y-4">
                    {filteredFollowUps.map((followUp) => (
                        <div
                            key={followUp.id}
                            className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow"
                        >
                            <div className="p-6">
                                {/* Header with action badge */}
                                <div className="flex items-start justify-between mb-4">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-2">
                                            <h3 className="text-xl font-semibold text-gray-900">
                                                {followUp.lead_name}
                                            </h3>
                                            <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-semibold rounded-full">
                                                {followUp.action || 'Follow-up'}
                                            </span>
                                            {followUp.metadata?.priority && (
                                                <span className={`px-3 py-1 text-xs font-bold rounded-full ${getPriorityColor(followUp.metadata.priority)}`}>
                                                    {followUp.metadata.priority.toUpperCase()}
                                                </span>
                                            )}
                                            {followUp.status === 'completed' && (
                                                <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-bold rounded-full">
                                                    COMPLETED
                                                </span>
                                            )}
                                            {followUp.metadata?.snoozed && (
                                                <span className="px-3 py-1 bg-purple-100 text-purple-800 text-xs font-bold rounded-full">
                                                    SNOOZED
                                                </span>
                                            )}
                                            {followUp.reason && (
                                                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                                                    {followUp.reason.replace(/_/g, ' ')}
                                                </span>
                                            )}
                                        </div>
                                        <p className="text-gray-600">{followUp.message}</p>
                                    </div>
                                </div>

                                {/* Contact Information */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
                                    <div className="space-y-2">
                                        <div className="flex items-center gap-2 text-gray-700">
                                            <Phone className="w-4 h-4" />
                                            <a
                                                href={`tel:${followUp.lead_phone}`}
                                                className="hover:text-blue-600 font-medium"
                                            >
                                                {followUp.lead_phone || 'No phone'}
                                            </a>
                                        </div>
                                        <div className="flex items-center gap-2 text-gray-700">
                                            <Mail className="w-4 h-4" />
                                            <a
                                                href={`mailto:${followUp.lead_email}`}
                                                className="hover:text-blue-600"
                                            >
                                                {followUp.lead_email || 'No email'}
                                            </a>
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        {followUp.lead_company && (
                                            <div className="flex items-center gap-2 text-gray-700">
                                                <Building2 className="w-4 h-4" />
                                                <span>{followUp.lead_company}</span>
                                            </div>
                                        )}
                                        <div className="flex items-center gap-2 text-gray-700">
                                            <Calendar className="w-4 h-4" />
                                            <span>
                                                {formatIST(followUp.scheduled_for) || 'ASAP'}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                {/* Products */}
                                {followUp.products && followUp.products.length > 0 && (
                                    <div className="mb-4">
                                        <p className="text-sm font-semibold text-gray-700 mb-2">
                                            Products of Interest:
                                        </p>
                                        <div className="flex flex-wrap gap-2">
                                            {followUp.products.map((product, idx) => (
                                                <span
                                                    key={idx}
                                                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                                                >
                                                    {product}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Lead Details */}
                                <div className="flex items-center gap-4 mb-4 text-sm text-gray-600">
                                    <span className="font-medium">Role: {followUp.lead_role || 'N/A'}</span>
                                    <span>•</span>
                                    <span>Status: {followUp.lead_status || 'new'}</span>
                                    <span>•</span>
                                    <span>Created: {formatDateIST(followUp.created_at)}</span>
                                </div>

                                {/* Action Buttons - Only show for pending */}
                                {followUp.status !== 'completed' && (
                                    <div className="flex gap-3 pt-4 border-t border-gray-200">
                                        <button
                                            onClick={() => handleComplete(followUp.id)}
                                            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                                        >
                                            <CheckCircle className="w-4 h-4" />
                                            Mark Complete
                                        </button>
                                        {!followUp.metadata?.snoozed && (
                                            <button
                                                onClick={() => handleSnooze(followUp.id)}
                                                className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                                            >
                                                <Clock className="w-4 h-4" />
                                                Snooze
                                            </button>
                                        )}
                                        <a
                                            href={`tel:${followUp.lead_phone}`}
                                            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                                        >
                                            <Phone className="w-4 h-4" />
                                            Call Now
                                        </a>
                                        <a
                                            href={`mailto:${followUp.lead_email}`}
                                            className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                                        >
                                            <Mail className="w-4 h-4" />
                                            Send Email
                                        </a>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Empty State */}
                {filteredFollowUps.length === 0 && (
                    <div className="bg-white rounded-lg shadow p-12 text-center">
                        <div className="text-6xl mb-4">
                            {filter === 'completed' ? '✅' : filter === 'snoozed' ? '😴' : '🎉'}
                        </div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                            {filter === 'completed' ? 'No completed tasks' :
                                filter === 'snoozed' ? 'No snoozed tasks' :
                                    `No ${filter} priority follow-ups!`}
                        </h3>
                        <p className="text-gray-600">
                            {filter === 'completed' ? 'Complete some tasks to see them here.' :
                                filter === 'snoozed' ? 'Snooze a follow-up to see it here.' :
                                    `All ${filter} priority tasks are handled!`}
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
