import React from 'react'
import OrderList from '../components/OrderList'

const OrdersPage = () => {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-semibold text-gray-900">Orders</h1>
                <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium shadow-sm transition-colors">
                    Create Order
                </button>
            </div>
            <OrderList />
        </div>
    )
}

export default OrdersPage
