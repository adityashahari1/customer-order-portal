import React from 'react'
import { revenueData } from '../services/mockData'

const SimpleBarChart = () => {
    const data = revenueData
    const maxValue = Math.max(...data.map(d => d.revenue))

    return (
        <div className="w-full">
            <div className="flex items-end justify-between h-64 w-full space-x-4 px-4">
                {data.map((item) => (
                    <div key={item.label} className="flex flex-col items-center flex-1 group h-full justify-end">
                        <div className="w-full flex space-x-1 items-end justify-center h-full">
                            {/* Revenue Bar */}
                            <div
                                className="w-1/2 bg-indigo-500 rounded-t-sm transition-all duration-500 relative hover:bg-indigo-600"
                                style={{ height: `${(item.revenue / maxValue) * 100}%` }}
                            >
                                <div className="opacity-0 group-hover:opacity-100 absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs rounded py-1 px-2 transition-opacity duration-200 z-10 whitespace-nowrap">
                                    Rev: ${item.revenue}
                                </div>
                            </div>
                            {/* Cost Bar */}
                            <div
                                className="w-1/2 bg-gray-300 rounded-t-sm transition-all duration-500 relative hover:bg-gray-400"
                                style={{ height: `${(item.cost / maxValue) * 100}%` }}
                            >
                                <div className="opacity-0 group-hover:opacity-100 absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs rounded py-1 px-2 transition-opacity duration-200 z-10 whitespace-nowrap">
                                    Cost: ${item.cost}
                                </div>
                            </div>
                        </div>
                        <div className="mt-2 text-xs text-gray-500 font-medium">{item.label}</div>
                    </div>
                ))}
            </div>
            <div className="flex justify-center mt-4 space-x-6">
                <div className="flex items-center">
                    <div className="w-3 h-3 bg-indigo-500 rounded-sm mr-2"></div>
                    <span className="text-xs text-gray-500">Revenue</span>
                </div>
                <div className="flex items-center">
                    <div className="w-3 h-3 bg-gray-300 rounded-sm mr-2"></div>
                    <span className="text-xs text-gray-500">Costs</span>
                </div>
            </div>
        </div>
    )
}

export default SimpleBarChart
