import React from 'react';
import { UserGroupIcon, StarIcon, MapPinIcon } from '@heroicons/react/24/outline';

const Professionals: React.FC = () => {
  const professionals = [
    {
      id: 1,
      name: 'John Smith',
      role: 'Tailor',
      experience: '15 years',
      rating: 4.9,
      reviews: 127,
      location: 'New York, NY',
      specialties: ['Suit Alterations', 'Formal Wear', 'Custom Tailoring'],
      image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    },
    {
      id: 2,
      name: 'Jane Doe',
      role: 'Fashion Designer',
      experience: '8 years',
      rating: 4.8,
      reviews: 89,
      location: 'Los Angeles, CA',
      specialties: ['Evening Wear', 'Wedding Dresses', 'Custom Design'],
      image: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    },
    {
      id: 3,
      name: 'Mike Johnson',
      role: 'Tailor',
      experience: '12 years',
      rating: 4.7,
      reviews: 95,
      location: 'Chicago, IL',
      specialties: ['Casual Wear', 'Denim Alterations', 'Leather Work'],
      image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-gray-900">Professional Tailors & Designers</h1>
          <p className="mt-1 text-sm text-gray-500">
            Connect with skilled professionals for your tailoring and fashion needs.
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
                placeholder="Search professionals..."
                className="input-field"
              />
            </div>
            <div className="flex space-x-3">
              <select className="input-field">
                <option>All Roles</option>
                <option>Tailor</option>
                <option>Fashion Designer</option>
              </select>
              <select className="input-field">
                <option>All Locations</option>
                <option>New York, NY</option>
                <option>Los Angeles, CA</option>
                <option>Chicago, IL</option>
              </select>
              <select className="input-field">
                <option>Sort by</option>
                <option>Rating</option>
                <option>Experience</option>
                <option>Reviews</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Professionals Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {professionals.map((professional) => (
          <div key={professional.id} className="bg-white shadow rounded-lg overflow-hidden">
            <div className="p-6">
              <div className="flex items-center space-x-4">
                <img
                  className="h-16 w-16 rounded-full object-cover"
                  src={professional.image}
                  alt={professional.name}
                />
                <div className="flex-1">
                  <h3 className="text-lg font-medium text-gray-900">{professional.name}</h3>
                  <p className="text-sm text-gray-500 capitalize">{professional.role}</p>
                  <div className="flex items-center mt-1">
                    <MapPinIcon className="h-4 w-4 text-gray-400 mr-1" />
                    <span className="text-sm text-gray-500">{professional.location}</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center">
                    <StarIcon className="h-4 w-4 text-yellow-400" />
                    <span className="ml-1 text-sm font-medium text-gray-900">
                      {professional.rating}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">{professional.reviews} reviews</p>
                </div>
              </div>

              <div className="mt-4">
                <p className="text-sm text-gray-600">
                  <span className="font-medium">Experience:</span> {professional.experience}
                </p>
                <div className="mt-2">
                  <p className="text-sm font-medium text-gray-700">Specialties:</p>
                  <div className="mt-1 flex flex-wrap gap-2">
                    {professional.specialties.map((specialty, index) => (
                      <span
                        key={index}
                        className="inline-flex px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full"
                      >
                        {specialty}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-6 flex space-x-3">
                <button className="btn-primary flex-1">
                  View Profile
                </button>
                <button className="btn-secondary flex-1">
                  Book Service
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {professionals.length === 0 && (
        <div className="text-center py-12">
          <UserGroupIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No professionals found</h3>
          <p className="mt-1 text-sm text-gray-500">Try adjusting your search or filter criteria.</p>
        </div>
      )}
    </div>
  );
};

export default Professionals;
