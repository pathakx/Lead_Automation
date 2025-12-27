import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { supabase } from '../services/supabase';
import {
    BarChart,
    Bar,
    PieChart,
    Pie,
    Cell,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';

interface DashboardStats {
    total_leads: number;
    new_leads_today: number;
    pending_follow_ups: number;
    pending_approvals: number;
    sla_violations: number;
    avg_response_time_minutes: number;
    conversion_rate: number;
}

interface ConversionFunnel {
    new: number;
    contacted: number;
    nurturing: number;
    qualified: number;
    converted: number;
    lost: number;
}

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [funnel, setFunnel] = useState<ConversionFunnel | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboardData();
        const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30s

        // Real-time subscription to leads table
        const subscription = supabase
            .channel('leads-changes')
            .on(
                'postgres_changes',
                { event: '*', schema: 'public', table: 'leads' },
                (payload) => {
                    console.log('Lead changed:', payload);
                    fetchDashboardData(); // Refresh dashboard on any lead change
                }
            )
            .subscribe();

        return () => {
            clearInterval(interval);
            subscription.unsubscribe();
        };
    }, []);

    const fetchDashboardData = async () => {
        try {
            const [statsRes, funnelRes] = await Promise.all([
                api.get('/api/analytics/dashboard'),
                api.get('/api/analytics/conversion')
            ]);
            setStats(statsRes.data);
            setFunnel(funnelRes.data);
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="text-xl text-gray-600">Loading dashboard...</div>
            </div>
        );
    }

    const funnelData = funnel ? [
        { name: 'New', value: funnel.new, color: '#3b82f6' },
        { name: 'Contacted', value: funnel.contacted, color: '#8b5cf6' },
        { name: 'Nurturing', value: funnel.nurturing, color: '#ec4899' },
        { name: 'Qualified', value: funnel.qualified, color: '#f59e0b' },
        { name: 'Converted', value: funnel.converted, color: '#10b981' },
        { name: 'Lost', value: funnel.lost, color: '#ef4444' }
    ] : [];

    return (
        <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total Leads"
                    value={stats?.total_leads || 0}
                    icon="📊"
                    color="blue"
                />
                <StatCard
                    title="New Today"
                    value={stats?.new_leads_today || 0}
                    icon="🆕"
                    color="green"
                />
                <StatCard
                    title="Pending Follow-ups"
                    value={stats?.pending_follow_ups || 0}
                    icon="📅"
                    color="yellow"
                />
                <StatCard
                    title="SLA Violations"
                    value={stats?.sla_violations || 0}
                    icon="⚠️"
                    color="red"
                />
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Conversion Funnel */}
                <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-semibold mb-4">Conversion Funnel</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={funnelData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="value" fill="#3b82f6" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Status Distribution */}
                <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-lg font-semibold mb-4">Status Distribution</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={funnelData}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={(entry) => entry.name}
                                outerRadius={80}
                                fill="#8884d8"
                                dataKey="value"
                            >
                                {funnelData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <MetricCard
                    title="Avg Response Time"
                    value={`${stats?.avg_response_time_minutes || 0} min`}
                    trend="down"
                />
                <MetricCard
                    title="Conversion Rate"
                    value={`${stats?.conversion_rate || 0}%`}
                    trend="up"
                />
                <MetricCard
                    title="Pending Approvals"
                    value={stats?.pending_approvals || 0}
                    trend="neutral"
                />
            </div>
        </div>
    );
}

function StatCard({ title, value, icon, color }: any) {
    const colors = {
        blue: 'bg-blue-100 text-blue-600',
        green: 'bg-green-100 text-green-600',
        yellow: 'bg-yellow-100 text-yellow-600',
        red: 'bg-red-100 text-red-600'
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm text-gray-600 mb-1">{title}</p>
                    <p className="text-3xl font-bold">{value}</p>
                </div>
                <div className={`text-4xl p-3 rounded-lg ${colors[color as keyof typeof colors]}`}>
                    {icon}
                </div>
            </div>
        </div>
    );
}

function MetricCard({ title, value, trend }: any) {
    const trendColors = {
        up: 'text-green-600',
        down: 'text-red-600',
        neutral: 'text-gray-600'
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow">
            <p className="text-sm text-gray-600 mb-2">{title}</p>
            <p className={`text-2xl font-bold ${trendColors[trend as keyof typeof trendColors]}`}>
                {value}
            </p>
        </div>
    );
}
