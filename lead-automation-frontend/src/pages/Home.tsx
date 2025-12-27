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
