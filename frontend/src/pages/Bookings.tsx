import React from 'react';
import { CalendarIcon, ClockIcon, MapPinIcon } from '@heroicons/react/24/outline';

const Bookings: React.FC = () => {
  const bookings = [
    {
      id: 1,
      service: 'Suit Alteration',
      professional: 'John Tailor',
      date: '2024-01-15',
      time: '10:00 AM',
      location: '123 Main St, City',
      status: 'Confirmed',
      notes: 'Please make the sleeves shorter',
    },
    {
      id: 2,
      service: 'Dress Design',
      professional: 'Jane Designer',
      date: '2024-01-18',
      time: '2:00 PM',
      location: '456 Oak Ave, City',
      status: 'Pending',
      notes: 'Custom evening dress for wedding',
    },
    {
      id: 3,
      service: 'Fabric Supply',
      professional: 'Bob Vendor',
      date: '2024-01-20',
      time: '11:00 AM',
      location: '789 Pine St, City',
      status: 'Completed',
      notes: 'Silk fabric for dress project',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Confirmed':
        return 'bg-green-100 text-green-800';
      case 'Pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'Completed':
        return 'bg-blue-100 text-blue-800';
      case 'Cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-gray-900">My Bookings</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your service bookings and appointments.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {bookings.map((booking) => (
          <div key={booking.id} className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-medium text-gray-900">{booking.service}</h3>
                  <p className="text-sm text-gray-500">with {booking.professional}</p>
                </div>
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(booking.status)}`}>
                  {booking.status}
                </span>
              </div>

              <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div className="flex items-center">
                  <CalendarIcon className="h-5 w-5 text-gray-400 mr-2" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{booking.date}</p>
                    <p className="text-sm text-gray-500">Date</p>
                  </div>
                </div>

                <div className="flex items-center">
                  <ClockIcon className="h-5 w-5 text-gray-400 mr-2" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{booking.time}</p>
                    <p className="text-sm text-gray-500">Time</p>
                  </div>
                </div>

                <div className="flex items-center">
                  <MapPinIcon className="h-5 w-5 text-gray-400 mr-2" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{booking.location}</p>
                    <p className="text-sm text-gray-500">Location</p>
                  </div>
                </div>
              </div>

              {booking.notes && (
                <div className="mt-4">
                  <p className="text-sm text-gray-500">Notes:</p>
                  <p className="text-sm text-gray-900">{booking.notes}</p>
                </div>
              )}

              <div className="mt-4 flex space-x-3">
                <button className="btn-primary text-sm">
                  View Details
                </button>
                {booking.status === 'Pending' && (
                  <button className="btn-secondary text-sm">
                    Cancel
                  </button>
                )}
                {booking.status === 'Completed' && (
                  <button className="btn-secondary text-sm">
                    Rate Service
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {bookings.length === 0 && (
        <div className="text-center py-12">
          <CalendarIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No bookings</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by booking a service.</p>
          <div className="mt-6">
            <button className="btn-primary">
              Browse Services
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Bookings;
