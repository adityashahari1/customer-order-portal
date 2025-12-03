import React, { useState } from 'react'
import { growthData } from '../services/mockData'

const SimpleLineChart = () => {
    const data = growthData
    const [hoveredPoint, setHoveredPoint] = useState<number | null>(null)

    if (!data || data.length === 0) {
        return <div className="h-64 flex items-center justify-center text-gray-500">No data available</div>
    }

    const maxValue = Math.max(...data.map(d => d.value))
    const padding = 10
    const width = 1000
    const height = 100
    
    const points = data.map((d, i) => {
        const x = padding + (i / (data.length - 1)) * (width - padding * 2)
        const y = padding + (1 - d.value / maxValue) * (height - padding * 2)
        return `${x},${y}`
    }).join(' ')

    return (
        <div className="w-full h-64 relative bg-gray-50 rounded-lg border border-gray-100">
            <div className="absolute inset-0 p-4 pb-10">
                <svg className="w-full h-full" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="xMidYMid meet">
                    {/* Grid lines */}
                    {[0, 25, 50, 75, 100].map(y => (
                        <line key={y} x1={padding} y1={y} x2={width - padding} y2={y} stroke="#e5e7eb" strokeWidth="0.3" />
                    ))}

                    {/* Line */}
                    <polyline
                        fill="none"
                        stroke="#6366f1"
                        strokeWidth="2"
                        points={points}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />

                    {/* Area under the line (optional gradient effect) */}
                    <polygon
                        fill="rgba(99, 102, 241, 0.1)"
                        points={`${padding},${height - padding} ${points} ${width - padding},${height - padding}`}
                    />

                    {/* Points with Tooltips */}
                    {data.map((d, i) => {
                        const x = padding + (i / (data.length - 1)) * (width - padding * 2)
                        const y = padding + (1 - d.value / maxValue) * (height - padding * 2)
                        const pointPercent = (x / width) * 100
                        const yPercent = (y / height) * 100
                        return (
                            <g key={i}>
                                <circle
                                    cx={x}
                                    cy={y}
                                    r="4"
                                    fill="#4f46e5"
                                    stroke="white"
                                    strokeWidth="2"
                                    className="transition-all duration-200 cursor-pointer"
                                    style={{ r: hoveredPoint === i ? '6' : '4' }}
                                    onMouseEnter={() => setHoveredPoint(i)}
                                    onMouseLeave={() => setHoveredPoint(null)}
                                />
                                {hoveredPoint === i && (
                                    <g>
                                        <rect
                                            x={x - 25}
                                            y={y - 35}
                                            width="50"
                                            height="25"
                                            fill="#1f2937"
                                            rx="4"
                                            opacity="0.95"
                                        />
                                        <text
                                            x={x}
                                            y={y - 18}
                                            textAnchor="middle"
                                            fill="white"
                                            fontSize="12"
                                            fontWeight="bold"
                                        >
                                            {d.value}%
                                        </text>
                                    </g>
                                )}
                            </g>
                        )
                    })}
                </svg>
            </div>

            {/* Labels */}
            <div className="absolute bottom-2 left-0 right-0 flex justify-between text-xs text-gray-500 px-6">
                {data.map(d => (
                    <span key={d.label}>{d.label}</span>
                ))}
            </div>
        </div>
    )
}

export default SimpleLineChart
