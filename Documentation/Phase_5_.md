# Phase 5: Frontend Development - Master Plan
## AI-Powered Lead Management Automation System

---

## 📅 Timeline: Days 8-12
**Status**: 🚀 Ready for Implementation  
**Last Updated**: December 27, 2024  
**Prerequisites**: Phase 4 completed (Backend API with all endpoints ready)

---

## 🎯 Phase 5 Objectives

### Primary Goal
Build a complete React frontend with public lead capture form, admin dashboard, leads management interface, approval queue, and analytics visualization. Integrate with backend APIs and implement real-time updates.

### Success Criteria
- ✅ Public lead form functional and responsive
- ✅ Admin dashboard with real-time metrics
- ✅ Leads management with filtering and search
- ✅ Approval queue for pending actions
- ✅ Analytics charts and visualizations
- ✅ All API integrations working
- ✅ Responsive design (mobile + desktop)
- ✅ Real-time updates implemented

---

## 📋 Deliverables

### 1. Public Pages
- ✅ Landing page with lead capture form
- ✅ Success confirmation page
- ✅ Responsive design

### 2. Admin Pages
- ✅ Dashboard with metrics and charts
- ✅ Leads list with filtering
- ✅ Lead detail view
- ✅ Approval queue
- ✅ Analytics page

### 3. Components
- ✅ LeadForm component
- ✅ Dashboard component
- ✅ LeadsList component
- ✅ LeadDetail component
- ✅ ApprovalQueue component
- ✅ Analytics component

### 4. Hooks & Services
- ✅ useLeads hook
- ✅ useApprovals hook
- ✅ API integration
- ✅ Real-time subscriptions

---

## 📝 Detailed Implementation Steps

## DAY 8-9: Core Components & Routing

### Step 1: Set Up React Router (30 minutes)

**Objective**: Configure routing for public and admin pages

**Install Dependencies**:
```bash
cd lead-automation-frontend
npm install react-router-dom
```

**Update `src/App.tsx`**:

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Admin from './pages/Admin';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**Verification**:
- [ ] React Router installed
- [ ] Routes configured
- [ ] Can navigate between pages

---

### Step 2: Create Lead Capture Form Component (90 minutes)

**Objective**: Build public-facing lead submission form

**File**: `src/components/LeadForm.tsx`

```tsx
import { useState } from 'react';
import { api } from '../services/api';

interface ProductInterest {
  category: string;
  product: string;
  quantity?: string;
}

export default function LeadForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    role: '',
    location: '',
    message: ''
  });

  const [products, setProducts] = useState<ProductInterest[]>([
    { category: '', product: '', quantity: '' }
  ]);

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const categories = ['Flooring', 'Wall Panels', 'Lighting', 'Laminates'];
  const roles = ['Home Owner', 'Architect', 'Builder', 'Contractor'];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const submission = {
        ...formData,
        product_interests: products.filter(p => p.category && p.product)
      };

      await api.post('/leads', submission);
      setSuccess(true);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        role: '',
        location: '',
        message: ''
      });
      setProducts([{ category: '', product: '', quantity: '' }]);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit lead');
    } finally {
      setLoading(false);
    }
  };

  const addProduct = () => {
    setProducts([...products, { category: '', product: '', quantity: '' }]);
  };

  const removeProduct = (index: number) => {
    setProducts(products.filter((_, i) => i !== index));
  };

  const updateProduct = (index: number, field: keyof ProductInterest, value: string) => {
    const updated = [...products];
    updated[index] = { ...updated[index], [field]: value };
    setProducts(updated);
  };

  if (success) {
    return (
      <div className="max-w-2xl mx-auto p-8 bg-white rounded-lg shadow-lg">
        <div className="text-center">
          <div className="text-6xl mb-4">✅</div>
          <h2 className="text-3xl font-bold text-green-600 mb-4">
            Thank You!
          </h2>
          <p className="text-gray-600 mb-6">
            We've received your inquiry and will get back to you within 24 hours.
          </p>
          <button
            onClick={() => setSuccess(false)}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Submit Another Inquiry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold mb-6 text-gray-800">
          Get a Quote
        </h2>
        
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Contact Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Vikas Pathak"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email *
              </label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="vikas@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phone
              </label>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="+91 9876543210"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Role *
              </label>
              <select
                required
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select Role</option>
                {roles.map(role => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Mumbai, India"
              />
            </div>
          </div>

          {/* Product Interests */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Interests
            </label>
            {products.map((product, index) => (
              <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                <select
                  value={product.category}
                  onChange={(e) => updateProduct(index, 'category', e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Category</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>

                <input
                  type="text"
                  value={product.product}
                  onChange={(e) => updateProduct(index, 'product', e.target.value)}
                  placeholder="Product name"
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />

                <input
                  type="text"
                  value={product.quantity}
                  onChange={(e) => updateProduct(index, 'quantity', e.target.value)}
                  placeholder="Quantity"
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />

                <button
                  type="button"
                  onClick={() => removeProduct(index)}
                  className="px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200"
                  disabled={products.length === 1}
                >
                  Remove
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={addProduct}
              className="px-4 py-2 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200"
            >
              + Add Product
            </button>
          </div>

          {/* Message */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Message
            </label>
            <textarea
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Tell us about your project..."
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 font-semibold text-lg"
          >
            {loading ? 'Submitting...' : 'Submit Inquiry'}
          </button>
        </form>
      </div>
    </div>
  );
}
```

**Verification**:
- [ ] Form renders correctly
- [ ] Can add/remove products
- [ ] Form validation works
- [ ] Submission calls API
- [ ] Success message displays

---

### Step 3: Create Home Page (30 minutes)

**Objective**: Create landing page with lead form

**File**: `src/pages/Home.tsx`

```tsx
import LeadForm from '../components/LeadForm';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold text-gray-900">
            Lead Automation System
          </h1>
        </div>
      </header>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Get Your Quote Today
          </h2>
          <p className="text-xl text-gray-600">
            Fill out the form below and we'll get back to you within 24 hours
          </p>
        </div>

        {/* Lead Form */}
        <LeadForm />
      </div>

      {/* Footer */}
      <footer className="bg-white mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600">
          <p>© 2024 Lead Automation System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
```

**Verification**:
- [ ] Home page renders
- [ ] Lead form displays
- [ ] Responsive layout works

---

## DAY 9-10: Admin Dashboard & Components

### Step 4: Create Dashboard Component (120 minutes)

**Objective**: Build admin dashboard with metrics and charts

**Install Chart Library**:
```bash
npm install recharts
```

**File**: `src/components/Dashboard.tsx`

```tsx
import { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
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
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, funnelRes] = await Promise.all([
        api.get('/analytics/dashboard'),
        api.get('/analytics/conversion')
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
```

**Verification**:
- [ ] Dashboard renders
- [ ] Stats cards display
- [ ] Charts render correctly
- [ ] Auto-refresh works

---

### Step 5: Create Leads List Component (90 minutes)

**Objective**: Build leads management interface with filtering

**File**: `src/components/LeadsList.tsx`

```tsx
import { useState, useEffect } from 'react';
import { api } from '../services/api';

interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: string;
  location: string;
  status: string;
  created_at: string;
}

export default function LeadsList() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchLeads();
  }, [statusFilter]);

  const fetchLeads = async () => {
    try {
      const params = statusFilter ? { status: statusFilter } : {};
      const response = await api.get('/leads', { params });
      setLeads(response.data);
    } catch (error) {
      console.error('Failed to fetch leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredLeads = leads.filter(lead =>
    lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    lead.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const statusColors: Record<string, string> = {
    new: 'bg-blue-100 text-blue-800',
    contacted: 'bg-purple-100 text-purple-800',
    nurturing: 'bg-yellow-100 text-yellow-800',
    qualified: 'bg-green-100 text-green-800',
    converted: 'bg-emerald-100 text-emerald-800',
    lost: 'bg-red-100 text-red-800'
  };

  if (loading) {
    return <div className="text-center py-8">Loading leads...</div>;
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow flex gap-4">
        <input
          type="text"
          placeholder="Search by name or email..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Statuses</option>
          <option value="new">New</option>
          <option value="contacted">Contacted</option>
          <option value="nurturing">Nurturing</option>
          <option value="qualified">Qualified</option>
          <option value="converted">Converted</option>
          <option value="lost">Lost</option>
        </select>
      </div>

      {/* Leads Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredLeads.map((lead) => (
              <tr key={lead.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">{lead.name}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500">{lead.email}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500">{lead.role}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusColors[lead.status]}`}>
                    {lead.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(lead.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button className="text-blue-600 hover:text-blue-900">
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredLeads.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No leads found
        </div>
      )}
    </div>
  );
}
```

**Verification**:
- [ ] Leads list renders
- [ ] Search works
- [ ] Status filter works
- [ ] Table displays correctly

---

### Step 6: Create Admin Page (45 minutes)

**Objective**: Create admin panel with navigation

**File**: `src/pages/Admin.tsx`

```tsx
import { useState } from 'react';
import Dashboard from '../components/Dashboard';
import LeadsList from '../components/LeadsList';

export default function Admin() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'leads', label: 'Leads', icon: '👥' },
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
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
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
          {activeTab === 'approvals' && (
            <div className="bg-white p-8 rounded-lg shadow text-center">
              <p className="text-gray-600">Approvals component coming soon...</p>
            </div>
          )}
          {activeTab === 'analytics' && (
            <div className="bg-white p-8 rounded-lg shadow text-center">
              <p className="text-gray-600">Analytics component coming soon...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
```

**Verification**:
- [ ] Admin page renders
- [ ] Tab navigation works
- [ ] Components switch correctly

---

## DAY 10-11: Advanced Features

### Step 7: Create Approval Queue Component (60 minutes)

**Objective**: Build approval management interface

**File**: `src/components/ApprovalQueue.tsx`

```tsx
import { useState, useEffect } from 'react';
import { api } from '../services/api';

interface Approval {
  id: string;
  lead_id: string;
  type: string;
  status: string;
  message: string;
  created_at: string;
  metadata: any;
}

export default function ApprovalQueue() {
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApprovals();
  }, []);

  const fetchApprovals = async () => {
    try {
      const response = await api.get('/approvals/pending');
      setApprovals(response.data);
    } catch (error) {
      console.error('Failed to fetch approvals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: string) => {
    try {
      await api.post(`/approvals/${id}/approve`, {
        notes: 'Approved from admin panel'
      });
      fetchApprovals(); // Refresh list
    } catch (error) {
      console.error('Failed to approve:', error);
    }
  };

  const handleReject = async (id: string) => {
    const reason = prompt('Enter rejection reason:');
    if (!reason) return;

    try {
      await api.post(`/approvals/${id}/reject`, { reason });
      fetchApprovals(); // Refresh list
    } catch (error) {
      console.error('Failed to reject:', error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading approvals...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold">Pending Approvals</h2>
          <p className="text-gray-600 mt-1">
            {approvals.length} approval{approvals.length !== 1 ? 's' : ''} pending
          </p>
        </div>

        <div className="divide-y divide-gray-200">
          {approvals.map((approval) => (
            <div key={approval.id} className="p-6 hover:bg-gray-50">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded">
                      {approval.type}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(approval.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-gray-900 mb-2">{approval.message}</p>
                  {approval.metadata && (
                    <div className="text-sm text-gray-600">
                      <pre className="bg-gray-50 p-2 rounded">
                        {JSON.stringify(approval.metadata, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => handleApprove(approval.id)}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    ✓ Approve
                  </button>
                  <button
                    onClick={() => handleReject(approval.id)}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                  >
                    ✗ Reject
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {approvals.length === 0 && (
          <div className="p-8 text-center text-gray-500">
            No pending approvals
          </div>
        )}
      </div>
    </div>
  );
}
```

**Verification**:
- [ ] Approvals list renders
- [ ] Approve action works
- [ ] Reject action works
- [ ] List refreshes after action

---

### Step 8: Add Real-time Updates (Optional) (45 minutes)

**Objective**: Implement Supabase real-time subscriptions

**Update Dashboard Component**:

```tsx
// Add to Dashboard.tsx
import { useEffect } from 'react';
import { supabase } from '../services/supabase';

// Inside Dashboard component
useEffect(() => {
  // Subscribe to leads table changes
  const subscription = supabase
    .channel('leads-changes')
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'leads' },
      (payload) => {
        console.log('Lead changed:', payload);
        fetchDashboardData(); // Refresh dashboard
      }
    )
    .subscribe();

  return () => {
    subscription.unsubscribe();
  };
}, []);
```

**Verification**:
- [ ] Real-time subscription works
- [ ] Dashboard updates on new leads
- [ ] No memory leaks

---

## DAY 11-12: Polish & Testing

### Step 9: Add Loading States and Error Handling (60 minutes)

**Objective**: Improve UX with proper loading and error states

**Create Loading Component**:

**File**: `src/components/Loading.tsx`

```tsx
export default function Loading() {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );
}
```

**Create Error Component**:

**File**: `src/components/Error.tsx`

```tsx
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
```

**Verification**:
- [ ] Loading states display
- [ ] Error messages show
- [ ] Retry functionality works

---

### Step 10: Responsive Design Testing (45 minutes)

**Objective**: Ensure all pages work on mobile and desktop

**Test Checklist**:
- [ ] Home page responsive
- [ ] Lead form works on mobile
- [ ] Dashboard charts resize properly
- [ ] Leads table scrolls on mobile
- [ ] Admin navigation works on small screens
- [ ] All buttons are touch-friendly

**Add Mobile Menu** (if needed):

```tsx
// Add to Admin.tsx for mobile navigation
const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
```

---

### Step 11: Final Integration Testing (60 minutes)

**Objective**: Test complete user flows

**Test Scenarios**:

1. **Public Lead Submission**:
   - [ ] Fill out lead form
   - [ ] Submit successfully
   - [ ] See success message
   - [ ] Verify lead appears in admin

2. **Admin Dashboard**:
   - [ ] View dashboard metrics
   - [ ] Charts display correctly
   - [ ] Stats are accurate

3. **Lead Management**:
   - [ ] Search for leads
   - [ ] Filter by status
   - [ ] View lead details

4. **Approval Workflow**:
   - [ ] View pending approvals
   - [ ] Approve an item
   - [ ] Reject an item
   - [ ] Verify status updates

**Create Test Script**:

**File**: `test_frontend.md`

```markdown
# Frontend Testing Checklist

## Public Pages
- [ ] Home page loads
- [ ] Lead form validates input
- [ ] Can submit lead
- [ ] Success message displays
- [ ] Form resets after submission

## Admin Pages
- [ ] Can navigate to /admin
- [ ] Dashboard loads with data
- [ ] Charts render correctly
- [ ] Leads list displays
- [ ] Can filter and search leads
- [ ] Approval queue shows pending items
- [ ] Can approve/reject items

## Responsive Design
- [ ] Works on mobile (375px)
- [ ] Works on tablet (768px)
- [ ] Works on desktop (1920px)

## Performance
- [ ] Pages load in < 2s
- [ ] No console errors
- [ ] Charts animate smoothly
```

---

## 🎯 Phase 5 Completion Checklist

### Core Components ✅
- [ ] LeadForm component
- [ ] Dashboard component
- [ ] LeadsList component
- [ ] ApprovalQueue component
- [ ] Loading component
- [ ] Error component

### Pages ✅
- [ ] Home page with lead form
- [ ] Admin page with navigation
- [ ] Responsive layouts

### Features ✅
- [ ] Lead submission working
- [ ] Dashboard with real-time stats
- [ ] Leads filtering and search
- [ ] Approval management
- [ ] Charts and visualizations
- [ ] Real-time updates (optional)

### Integration ✅
- [ ] All API endpoints connected
- [ ] Error handling implemented
- [ ] Loading states added
- [ ] Responsive design verified

### Testing ✅
- [ ] All user flows tested
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Performance acceptable

---

## 📁 Files Created/Modified

### Components
1. **`src/components/LeadForm.tsx`** (NEW)
2. **`src/components/Dashboard.tsx`** (NEW)
3. **`src/components/LeadsList.tsx`** (NEW)
4. **`src/components/ApprovalQueue.tsx`** (NEW)
5. **`src/components/Loading.tsx`** (NEW)
6. **`src/components/Error.tsx`** (NEW)

### Pages
7. **`src/pages/Home.tsx`** (NEW)
8. **`src/pages/Admin.tsx`** (NEW)

### Configuration
9. **`src/App.tsx`** (MODIFIED) - Router setup

---

## 🔧 Dependencies to Install

```bash
npm install react-router-dom
npm install recharts
```

---

## 🚀 What's Next: Phase 6

Phase 5 frontend is complete! Ready for:

**Phase 6: AI Integration & Workflows**
- Test AI categorization accuracy
- Validate email sequences
- Configure automation rules
- Test follow-up logic
- Verify escalation rules

---

## 📝 Notes

- All components use TailwindCSS for styling
- Charts use Recharts library
- Real-time updates use Supabase subscriptions
- Error handling at component level
- Loading states for better UX
- Mobile-first responsive design

**Phase 5 Status: Ready for Implementation** (11 steps total)
