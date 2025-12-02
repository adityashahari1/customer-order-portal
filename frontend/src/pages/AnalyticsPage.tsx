import React from 'react'
import { BarChart2, TrendingUp, Users, DollarSign } from 'lucide-react'
import SimpleLineChart from '../components/SimpleLineChart'

const AnalyticsPage = () => {
    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-semibold text-gray-900">Analytics Dashboard</h1>

            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                <div className="bg-white overflow-hidden shadow rounded-lg p-5">
                    <div className="flex items-center">
                        <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                            <TrendingUp className="h-6 w-6 text-white" />
                        </div>
                        <div className="ml-5 w-0 flex-1">
                            <dl>
                                <dt className="text-sm font-medium text-gray-500 truncate">Growth Rate</dt>
                                <dd className="text-2xl font-semibold text-gray-900">+12.5%</dd>
                            </dl>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg p-5">
                    <div className="flex items-center">
                        <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                            <DollarSign className="h-6 w-6 text-white" />
                        </div>
                        <div className="ml-5 w-0 flex-1">
                            <dl>
                                <dt className="text-sm font-medium text-gray-500 truncate">Avg. Order Value</dt>
                                <dd className="text-2xl font-semibold text-gray-900">$85.00</dd>
                            </dl>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg p-5">
                    <div className="flex items-center">
                        <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                            <Users className="h-6 w-6 text-white" />
                        </div>
                        <div className="ml-5 w-0 flex-1">
                            <dl>
                                <dt className="text-sm font-medium text-gray-500 truncate">New Customers</dt>
                                <dd className="text-2xl font-semibold text-gray-900">128</dd>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Sales Growth (YTD)</h3>
                <SimpleLineChart />
            </div>
        </div>
    )
}

export default AnalyticsPage
