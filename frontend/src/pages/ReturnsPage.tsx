import React, { useState, useEffect } from 'react'
import { RotateCcw, CheckCircle, XCircle, Clock } from 'lucide-react'

interface Return {
    id: number
    order_id: number
    reason: string
    status: string
    refund_amount: number
    created_at: string
}

const ReturnsPage = () => {
    const [returns, setReturns] = useState<Return[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchReturns = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/returns/')
                if (!response.ok) {
                    throw new Error('Failed to fetch returns')
                }
                const data = await response.json()
                setReturns(data)
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred')
            } finally {
                setLoading(false)
            }
        }

        fetchReturns()
    }, [])

    const getStatusIcon = (status: string) => {
        switch (status.toUpperCase()) {
            case 'APPROVED':
            case 'COMPLETED':
                return <CheckCircle className="h-5 w-5 text-green-500" />
            case 'REJECTED':
                return <XCircle className="h-5 w-5 text-red-500" />
            case 'REQUESTED':
            case 'PENDING':
                return <Clock className="h-5 w-5 text-yellow-500" />
            default:
                return <RotateCcw className="h-5 w-5 text-gray-500" />
        }
    }

    if (loading) {
        return (
            <div className="bg-white shadow overflow-hidden sm:rounded-md p-8 text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
                <p className="mt-2 text-gray-500">Loading returns...</p>
            </div>
        )
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-red-800">Error: {error}</p>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-semibold text-gray-900">Returns</h1>
            </div>

            <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                    {returns.map((returnItem) => (
                        <li key={returnItem.id}>
                            <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors cursor-pointer">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center truncate">
                                        <div className="flex-shrink-0 mr-3">
                                            {getStatusIcon(returnItem.status)}
                                        </div>
                                        <p className="text-sm font-medium text-indigo-600 truncate">
                                            Return #{returnItem.id} - Order #{returnItem.order_id}
                                        </p>
                                    </div>
                                    <div className="ml-2 flex-shrink-0 flex">
                                        <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${returnItem.status.toUpperCase() === 'APPROVED' || returnItem.status.toUpperCase() === 'COMPLETED'
                                                ? 'bg-green-100 text-green-800'
                                                : returnItem.status.toUpperCase() === 'REQUESTED' || returnItem.status.toUpperCase() === 'PENDING'
                                                    ? 'bg-yellow-100 text-yellow-800'
                                                    : 'bg-red-100 text-red-800'
                                            }`}>
                                            {returnItem.status}
                                        </p>
                                    </div>
                                </div>
                                <div className="mt-2 sm:flex sm:justify-between">
                                    <div className="sm:flex">
                                        <p className="flex items-center text-sm text-gray-500">
                                            Reason: {returnItem.reason}
                                        </p>
                                    </div>
                                    <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                                        <p>
                                            Refund: <span className="font-medium text-gray-900">${returnItem.refund_amount.toFixed(2)}</span>
                                        </p>
                                        <p className="ml-6">
                                            {new Date(returnItem.created_at).toLocaleDateString()}
                                        </p>
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

export default ReturnsPage
