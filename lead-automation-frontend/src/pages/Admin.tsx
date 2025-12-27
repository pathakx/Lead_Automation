import { useState } from 'react';
import Dashboard from '../components/Dashboard';
import LeadsList from '../components/LeadsList';
import ApprovalQueue from '../components/ApprovalQueue';
import FollowUpQueue from '../components/FollowUpQueue';

export default function Admin() {
    const [activeTab, setActiveTab] = useState('dashboard');

    const tabs = [
        { id: 'dashboard', label: 'Dashboard', icon: '📊' },
        { id: 'leads', label: 'Leads', icon: '👥' },
        { id: 'followups', label: 'Follow-ups', icon: '📅' },
        { id: 'approvals', label: 'Approvals', icon: '✅' },
        { id: 'analytics', label: 'Analytics', icon: '📈' }
    ];

    return (
        <div className="min-h-screen bg-gray-100">
            {/* Header */}
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 py-6">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Admin Panel
                    </h1>
                </div>
            </header>

            {/* Navigation Tabs */}
            <div className="max-w-7xl mx-auto px-4 py-6">
                <div className="bg-white rounded-lg shadow mb-6">
                    <nav className="flex space-x-4 p-4">
                        {tabs.map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === tab.id
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                    }`}
                            >
                                <span className="mr-2">{tab.icon}</span>
                                {tab.label}
                            </button>
                        ))}
                    </nav>
                </div>

                {/* Content */}
                <div>
                    {activeTab === 'dashboard' && <Dashboard />}
                    {activeTab === 'leads' && <LeadsList />}
                    {activeTab === 'followups' && <FollowUpQueue />}
                    {activeTab === 'approvals' && <ApprovalQueue />}
                    {activeTab === 'analytics' && (
                        <div className="bg-white p-8 rounded-lg shadow text-center">
                            <p className="text-gray-600">Additional analytics coming soon...</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
