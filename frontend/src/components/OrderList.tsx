import React, { useState, useEffect } from 'react'
import { CheckCircle, Clock, Truck, XCircle, AlertCircle } from 'lucide-react'

interface OrderItem {
    id: number
    product_id: number
    quantity: number
    price: number
    order_id: number
}

interface Order {
    id: number
    status: string
    customer_name?: string
    items: OrderItem[]
    total_amount: number
    created_at: string
    user_id: number
}

const OrderList = () => {
    const [orders, setOrders] = useState<Order[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/orders/')
                if (!response.ok) {
                    throw new Error('Failed to fetch orders')
                }
                const data = await response.json()
                setOrders(data)
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred')
            } finally {
                setLoading(false)
            }
        }

        fetchOrders()
    }, [])

    const getStatusIcon = (status: string) => {
        switch (status.toUpperCase()) {
            case 'DELIVERED':
                return <CheckCircle className="h-5 w-5 text-green-500" />
            case 'PROCESSING':
                return <Clock className="h-5 w-5 text-yellow-500" />
            case 'SHIPPED':
                return <Truck className="h-5 w-5 text-blue-500" />
            case 'PENDING':
                return <AlertCircle className="h-5 w-5 text-gray-500" />
            case 'CANCELLED':
                return <XCircle className="h-5 w-5 text-red-500" />
            default:
                return <Clock className="h-5 w-5 text-gray-500" />
        }
    }

    if (loading) {
        return (
            <div className="bg-white shadow overflow-hidden sm:rounded-md p-8 text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
                <p className="mt-2 text-gray-500">Loading orders...</p>
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
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
                {orders.map((order) => (
                    <li key={order.id}>
                        <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors cursor-pointer">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center truncate">
                                    <div className="flex-shrink-0 mr-3">
                                        {getStatusIcon(order.status)}
                                    </div>
                                    <p className="text-sm font-medium text-indigo-600 truncate">Order #{order.id}</p>
                                </div>
                                <div className="ml-2 flex-shrink-0 flex">
                                    <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${order.status.toUpperCase() === 'DELIVERED' ? 'bg-green-100 text-green-800' :
                                        order.status.toUpperCase() === 'PROCESSING' ? 'bg-yellow-100 text-yellow-800' :
                                            order.status.toUpperCase() === 'SHIPPED' ? 'bg-blue-100 text-blue-800' :
                                                'bg-gray-100 text-gray-800'
                                        }`}>
                                        {order.status}
                                    </p>
                                </div>
                            </div>
                            <div className="mt-2 sm:flex sm:justify-between">
                                <div className="sm:flex">
                                    <p className="flex items-center text-sm text-gray-500">
                                        {order.customer_name || `User #${order.user_id}`}
                                    </p>
                                    <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                                        {order.items?.length || 0} items
                                    </p>
                                </div>
                                <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                                    <p>
                                        Total: <span className="font-medium text-gray-900">${order.total_amount.toFixed(2)}</span>
                                    </p>
                                    <p className="ml-6">
                                        {new Date(order.created_at).toLocaleDateString()}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default OrderList
