import React from 'react';
import { ShoppingBagIcon, StarIcon } from '@heroicons/react/24/outline';

const Marketplace: React.FC = () => {
  const products = [
    {
      id: 1,
      name: 'Premium Silk Fabric',
      vendor: 'Fabric World',
      price: 45.99,
      image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      rating: 4.8,
      reviews: 124,
    },
    {
      id: 2,
      name: 'Cotton Thread Set',
      vendor: 'Thread Master',
      price: 12.50,
      image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      rating: 4.6,
      reviews: 89,
    },
    {
      id: 3,
      name: 'Designer Buttons',
      vendor: 'Button Boutique',
      price: 8.99,
      image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      rating: 4.9,
      reviews: 67,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-gray-900">Marketplace</h1>
          <p className="mt-1 text-sm text-gray-500">
            Discover quality fabrics, materials, and supplies from trusted vendors.
          </p>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div className="flex-1 max-w-lg">
              <input
                type="text"
                placeholder="Search products..."
                className="input-field"
              />
            </div>
            <div className="flex space-x-3">
              <select className="input-field">
                <option>All Categories</option>
                <option>Fabrics</option>
                <option>Threads</option>
                <option>Buttons</option>
                <option>Accessories</option>
              </select>
              <select className="input-field">
                <option>Sort by</option>
                <option>Price: Low to High</option>
                <option>Price: High to Low</option>
                <option>Rating</option>
                <option>Newest</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {products.map((product) => (
          <div key={product.id} className="bg-white shadow rounded-lg overflow-hidden">
            <div className="aspect-w-16 aspect-h-9">
              <img
                className="w-full h-48 object-cover"
                src={product.image}
                alt={product.name}
              />
            </div>
            <div className="p-6">
              <h3 className="text-lg font-medium text-gray-900">{product.name}</h3>
              <p className="text-sm text-gray-500">by {product.vendor}</p>
              
              <div className="mt-2 flex items-center">
                <div className="flex items-center">
                  {[0, 1, 2, 3, 4].map((rating) => (
                    <StarIcon
                      key={rating}
                      className={`h-4 w-4 ${
                        rating < Math.floor(product.rating)
                          ? 'text-yellow-400'
                          : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>
                <span className="ml-2 text-sm text-gray-500">
                  {product.rating} ({product.reviews} reviews)
                </span>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <span className="text-2xl font-bold text-gray-900">${product.price}</span>
                <button className="btn-primary text-sm">
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {products.length === 0 && (
        <div className="text-center py-12">
          <ShoppingBagIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No products found</h3>
          <p className="mt-1 text-sm text-gray-500">Try adjusting your search or filter criteria.</p>
        </div>
      )}
    </div>
  );
};

export default Marketplace;
