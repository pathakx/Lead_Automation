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

            await api.post('/api/leads', submission);
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
