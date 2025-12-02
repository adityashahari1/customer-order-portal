import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './components/Dashboard'
import ChatWidget from './components/ChatWidget'
import OrdersPage from './pages/OrdersPage'
import InventoryPage from './pages/InventoryPage'
import CustomersPage from './pages/CustomersPage'
import AnalyticsPage from './pages/AnalyticsPage'
import ReturnsPage from './pages/ReturnsPage'

function App() {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/orders" element={<OrdersPage />} />
                    <Route path="/inventory" element={<InventoryPage />} />
                    <Route path="/customers" element={<CustomersPage />} />
                    <Route path="/returns" element={<ReturnsPage />} />
                    <Route path="/analytics" element={<AnalyticsPage />} />
                </Routes>
                <ChatWidget />
            </Layout>
        </Router>
    )
}

export default App
