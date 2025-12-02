import React from 'react'
import { growthData } from '../services/mockData'

const SimpleLineChart = () => {
    const data = growthData

    if (!data || data.length === 0) {
        return <div className="h-64 flex items-center justify-center text-gray-500">No data available</div>
    }

    const maxValue = 100
    const points = data.map((d, i) => {
        const x = (i / (data.length - 1)) * 100
        const y = 100 - (d.value / maxValue) * 100
        return `${x},${y}`
    }).join(' ')

    return (
        <div className="w-full h-64 relative px-4 pt-4 pb-8 bg-gray-50 rounded-lg border border-gray-100">
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 100 100">
                {/* Grid lines */}
                {[0, 25, 50, 75, 100].map(y => (
                    <line key={y} x1="0" y1={y} x2="100" y2={y} stroke="#e5e7eb" strokeWidth="1" vectorEffect="non-scaling-stroke" />
                ))}

                {/* Line */}
                <polyline
                    fill="none"
                    stroke="#6366f1"
                    strokeWidth="3"
                    points={points}
                    vectorEffect="non-scaling-stroke"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />

                {/* Area under the line (optional gradient effect) */}
                <polygon
                    fill="rgba(99, 102, 241, 0.1)"
                    points={`0,100 ${points} 100,100`}
                    vectorEffect="non-scaling-stroke"
                />

                {/* Points */}
                {data.map((d, i) => {
                    const x = (i / (data.length - 1)) * 100
                    const y = 100 - (d.value / maxValue) * 100
                    return (
                        <g key={i} className="group">
                            <circle
                                cx={x}
                                cy={y}
                                r="4"
                                fill="#4f46e5"
                                stroke="white"
                                strokeWidth="2"
                                vectorEffect="non-scaling-stroke"
                                className="transition-all duration-200 cursor-pointer group-hover:r-6"
                            />
                            {/* Tooltip */}
                            <foreignObject x={x - 20} y={y - 35} width="40" height="30" className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 overflow-visible">
                                <div className="bg-gray-900 text-white text-xs rounded py-1 px-2 text-center whitespace-nowrap transform -translate-x-1/2 left-1/2 relative">
                                    {d.value}%
                                </div>
                            </foreignObject>
                        </g>
                    )
                })}
            </svg>

            {/* Labels */}
            <div className="absolute bottom-2 left-0 right-0 flex justify-between text-xs text-gray-500 px-4">
                {data.map(d => (
                    <span key={d.label}>{d.label}</span>
                ))}
            </div>
        </div>
    )
}

export default SimpleLineChart
