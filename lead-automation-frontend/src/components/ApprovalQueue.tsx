import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Phone, Mail, Building2, User, Package, AlertTriangle, CheckCircle, XCircle, Clock } from 'lucide-react';
import { formatIST } from '../utils/dateUtils';

interface Approval {
    id: string;
    lead_id: string;
    type: string;
    status: string;
    message: string;
    created_at: string;
    metadata: {
        approval_type: string;
        lead_name: string;
        lead_email: string;
        lead_phone: string;
        lead_role: string;
        lead_company: string;
        priority: string;
        details: {
            message: string;
            products?: string[];
            total_quantity?: number;
            threshold?: number;
            role?: string;
            keywords_found?: string[];
            message_snippet?: string;
        };
    };
}

interface Stats {
    pending: number;
    approved: number;
    rejected: number;
    total: number;
}

export default function ApprovalQueue() {
    const [approvals, setApprovals] = useState<Approval[]>([]);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState<Stats>({ pending: 0, approved: 0, rejected: 0, total: 0 });
    const [filter, setFilter] = useState<'pending' | 'approved' | 'rejected'>('pending');

    useEffect(() => {
        fetchData();
        // Refresh every 30 seconds
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, [filter]);

    const fetchData = async () => {
        try {
            // Fetch stats
            const statsResponse = await api.get('/api/approvals/stats');
            setStats(statsResponse.data);

            // Fetch approvals based on filter
            const response = await api.get(`/api/approvals/${filter}`);
            setApprovals(response.data);
        } catch (error) {
            console.error('Failed to fetch approvals:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleApprove = async (id: string) => {
        const notes = prompt('Enter approval notes (optional):');
        try {
            await api.post(`/api/approvals/${id}/approve`, { notes: notes || 'Approved from admin panel' });
            fetchData(); // Refresh data
        } catch (error) {
            console.error('Failed to approve:', error);
            alert('Failed to approve');
        }
    };

    const handleReject = async (id: string) => {
        const reason = prompt('Enter rejection reason (required):');
        if (!reason) return;

        try {
            await api.post(`/api/approvals/${id}/reject`, { reason });
            fetchData(); // Refresh data
        } catch (error) {
            console.error('Failed to reject:', error);
            alert('Failed to reject');
        }
    };

    const getApprovalIcon = (type: string) => {
        switch (type) {
            case 'large_quantity_order':
                return '📦';
            case 'high_priority_professional':
                return '🏗️';
            case 'bulk_discount_request':
                return '💰';
            default:
                return '⚠️';
        }
    };

    const getApprovalTitle = (type: string) => {
        switch (type) {
            case 'large_quantity_order':
                return 'Large Quantity Order';
            case 'high_priority_professional':
                return 'High-Priority Professional';
            case 'bulk_discount_request':
                return 'Bulk Discount Request';
            default:
                return 'Approval Required';
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
        return <div className="text-center py-8">Loading approvals...</div>;
    }

    return (
        <div className="space-y-4">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Pending Card */}
                <button
                    onClick={() => setFilter('pending')}
                    className={`p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'pending' ? 'bg-yellow-50 border-2 border-yellow-400' : 'bg-white border-2 border-transparent'
                        }`}
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Pending Approvals</p>
                            <p className="text-3xl font-bold text-yellow-600 mt-2">{stats.pending}</p>
                        </div>
                        <Clock className="w-12 h-12 text-yellow-400" />
                    </div>
                </button>

                {/* Approved Card */}
                <button
                    onClick={() => setFilter('approved')}
                    className={`p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'approved' ? 'bg-green-50 border-2 border-green-400' : 'bg-white border-2 border-transparent'
                        }`}
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Approved</p>
                            <p className="text-3xl font-bold text-green-600 mt-2">{stats.approved}</p>
                        </div>
                        <CheckCircle className="w-12 h-12 text-green-400" />
                    </div>
                </button>

                {/* Rejected Card */}
                <button
                    onClick={() => setFilter('rejected')}
                    className={`p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left ${filter === 'rejected' ? 'bg-red-50 border-2 border-red-400' : 'bg-white border-2 border-transparent'
                        }`}
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Rejected</p>
                            <p className="text-3xl font-bold text-red-600 mt-2">{stats.rejected}</p>
                        </div>
                        <XCircle className="w-12 h-12 text-red-400" />
                    </div>
                </button>
            </div>

            {/* Header */}
            <div className="bg-white rounded-lg shadow p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900 capitalize">{filter} Approvals</h2>
                        <p className="text-gray-600 mt-1">
                            {approvals.length} {filter} approval{approvals.length !== 1 ? 's' : ''}
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

            {/* Approval Cards */}
            <div className="space-y-4">
                {approvals.map((approval) => (
                    <div
                        key={approval.id}
                        className={`bg-white rounded-lg shadow hover:shadow-lg transition-shadow border-l-4 ${approval.status === 'approved'
                            ? 'border-green-400'
                            : approval.status === 'rejected'
                                ? 'border-red-400'
                                : 'border-yellow-400'
                            }`}
                    >
                        <div className="p-6">
                            {/* Header */}
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <span className="text-3xl">
                                            {getApprovalIcon(approval.metadata?.approval_type)}
                                        </span>
                                        <div>
                                            <h3 className="text-xl font-semibold text-gray-900">
                                                {approval.metadata?.lead_name}
                                            </h3>
                                            <p className="text-sm text-gray-600">
                                                {getApprovalTitle(approval.metadata?.approval_type)}
                                            </p>
                                        </div>
                                        {approval.metadata?.priority && (
                                            <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getPriorityColor(approval.metadata.priority)}`}>
                                                {approval.metadata.priority.toUpperCase()}
                                            </span>
                                        )}
                                        {/* Status Badge */}
                                        {approval.status !== 'pending' && (
                                            <span className={`px-3 py-1 text-xs font-bold rounded-full ${approval.status === 'approved'
                                                ? 'bg-green-100 text-green-800'
                                                : 'bg-red-100 text-red-800'
                                                }`}>
                                                {approval.status.toUpperCase()}
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-gray-700 font-medium mb-3">{approval.message}</p>
                                </div>
                            </div>

                            {/* Customer Contact Info */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
                                <div className="space-y-2">
                                    <div className="flex items-center gap-2 text-gray-700">
                                        <Phone className="w-4 h-4" />
                                        <a href={`tel:${approval.metadata?.lead_phone}`} className="hover:text-blue-600 font-medium">
                                            {approval.metadata?.lead_phone || 'No phone'}
                                        </a>
                                    </div>
                                    <div className="flex items-center gap-2 text-gray-700">
                                        <Mail className="w-4 h-4" />
                                        <a href={`mailto:${approval.metadata?.lead_email}`} className="hover:text-blue-600">
                                            {approval.metadata?.lead_email}
                                        </a>
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    {approval.metadata?.lead_company && (
                                        <div className="flex items-center gap-2 text-gray-700">
                                            <Building2 className="w-4 h-4" />
                                            <span>{approval.metadata.lead_company}</span>
                                        </div>
                                    )}
                                    <div className="flex items-center gap-2 text-gray-700">
                                        <User className="w-4 h-4" />
                                        <span>{approval.metadata?.lead_role || 'No role'}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Approval Details */}
                            <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                                <h4 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
                                    <AlertTriangle className="w-4 h-4" />
                                    Approval Details
                                </h4>
                                <div className="space-y-2 text-sm">
                                    {approval.metadata?.details?.total_quantity && (
                                        <p className="text-blue-800">
                                            <strong>Total Quantity:</strong> {approval.metadata.details.total_quantity} units
                                            {approval.metadata.details.threshold && (
                                                <span className="text-xs ml-2">(Threshold: {approval.metadata.details.threshold})</span>
                                            )}
                                        </p>
                                    )}
                                    {approval.metadata?.details?.products && approval.metadata.details.products.length > 0 && (
                                        <div>
                                            <strong className="text-blue-800">Products:</strong>
                                            <div className="flex flex-wrap gap-2 mt-1">
                                                {approval.metadata.details.products.map((product, idx) => (
                                                    <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                                                        {product}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                    {approval.metadata?.details?.keywords_found && approval.metadata.details.keywords_found.length > 0 && (
                                        <p className="text-blue-800">
                                            <strong>Keywords Found:</strong> {approval.metadata.details.keywords_found.join(', ')}
                                        </p>
                                    )}
                                    {approval.metadata?.details?.message_snippet && (
                                        <p className="text-blue-800">
                                            <strong>Customer Message:</strong><br />
                                            <span className="italic text-gray-700">"{approval.metadata.details.message_snippet}"</span>
                                        </p>
                                    )}
                                </div>
                            </div>

                            {/* Timestamp */}
                            <p className="text-xs text-gray-500 mb-4">
                                {approval.status === 'pending' ? 'Created' : approval.status === 'approved' ? 'Approved' : 'Rejected'}: {new Date(approval.created_at).toLocaleString()}
                            </p>

                            {/* Action Buttons (Only for Pending) */}
                            {approval.status === 'pending' && (
                                <div className="flex gap-3 pt-4 border-t border-gray-200">
                                    <button
                                        onClick={() => handleApprove(approval.id)}
                                        className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-colors"
                                    >
                                        ✓ Approve
                                    </button>
                                    <button
                                        onClick={() => handleReject(approval.id)}
                                        className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium transition-colors"
                                    >
                                        ✗ Reject
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Empty State */}
            {approvals.length === 0 && (
                <div className="bg-white rounded-lg shadow p-12 text-center">
                    <div className="text-6xl mb-4">
                        {filter === 'pending' ? '✅' : filter === 'approved' ? '🎉' : '📝'}
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                        No {filter} approvals
                    </h3>
                    <p className="text-gray-600">
                        {filter === 'pending'
                            ? 'All approval requests have been processed!'
                            : filter === 'approved'
                                ? 'No approvals have been granted yet.'
                                : 'No approvals have been rejected yet.'}
                    </p>
                </div>
            )}
        </div>
    );
}
