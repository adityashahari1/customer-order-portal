import React from 'react'
import { Users, Mail, Phone, MapPin, MoreVertical, Search } from 'lucide-react'
import { customers } from '../services/mockData'

const CustomersPage = () => {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-semibold text-gray-900">Customer Directory</h1>
                <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium shadow-sm transition-colors flex items-center">
                    <Users className="h-4 w-4 mr-2" />
                    Add Customer
                </button>
            </div>

            {/* Search Bar */}
            <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-gray-400" />
                </div>
                <input
                    type="text"
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="Search customers by name, email, or phone..."
                />
            </div>

            <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                    {customers.map((customer) => (
                        <li key={customer.id}>
                            <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors cursor-pointer">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center min-w-0">
                                        <div className="flex-shrink-0 h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center">
                                            <span className="text-indigo-600 font-bold text-lg">{customer.name.charAt(0)}</span>
                                        </div>
                                        <div className="ml-4 min-w-0">
                                            <div className="text-sm font-medium text-indigo-600 truncate">{customer.name}</div>
                                            <div className="flex items-center text-sm text-gray-500 space-x-4 mt-1">
                                                <div className="flex items-center">
                                                    <Mail className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                                                    <span className="truncate">{customer.email}</span>
                                                </div>
                                                <div className="flex items-center">
                                                    <Phone className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                                                    <span>{customer.phone}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-8">
                                        <div className="hidden md:flex flex-col items-end">
                                            <div className="flex items-center text-sm text-gray-500 mb-1">
                                                <MapPin className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                                                {customer.location}
                                            </div>
                                            <div className="text-xs text-gray-400">Last Order: {customer.lastOrder}</div>
                                        </div>
                                        <div className="flex items-center space-x-4">
                                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${customer.status === 'Active' ? 'bg-green-100 text-green-800' :
                                                    customer.status === 'Blocked' ? 'bg-red-100 text-red-800' :
                                                        'bg-gray-100 text-gray-800'
                                                }`}>
                                                {customer.status}
                                            </span>
                                            <button className="text-gray-400 hover:text-gray-500">
                                                <MoreVertical className="h-5 w-5" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}

export default CustomersPage
