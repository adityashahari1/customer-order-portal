import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Layout from './components/Layout'
import Dashboard from './components/Dashboard'
import ChatWidget from './components/ChatWidget'
import OrdersPage from './pages/OrdersPage'
import InventoryPage from './pages/InventoryPage'
import CustomersPage from './pages/CustomersPage'
import AnalyticsPage from './pages/AnalyticsPage'
import ReturnsPage from './pages/ReturnsPage'
import Login from './components/Login'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
    return (
        <Router>
            <AuthProvider>
                <Routes>
                    {/* Public route */}
                    <Route path="/login" element={<Login />} />
                    
                    {/* Protected routes */}
                    <Route path="/" element={
                        <ProtectedRoute>
                            <Layout>
                                <Dashboard />
                                <ChatWidget />
                            </Layout>
                        </ProtectedRoute>
                    } />
                    <Route path="/orders" element={
                        <ProtectedRoute>
                            <Layout>
                                <OrdersPage />
                                <ChatWidget />
                            </Layout>
                        </ProtectedRoute>
                    } />
                    <Route path="/inventory" element={
                        <ProtectedRoute>
                            <Layout>
                                <InventoryPage />
                                <ChatWidget />
                            </Layout>
                        </ProtectedRoute>
                    } />
                    <Route path="/customers" element={
                        <ProtectedRoute>
                            <Layout>
                                <CustomersPage />
                                <ChatWidget />
                            </Layout>
                        </ProtectedRoute>
                    } />
                    <Route path="/returns" element={
                        <ProtectedRoute>
                            <Layout>
                                <ReturnsPage />
                                <ChatWidget />
                            </Layout>
                        </ProtectedRoute>
                    } />
                    <Route path="/analytics" element={
                        <ProtectedRoute>
                            <Layout>
                                <AnalyticsPage />
                                <ChatWidget />
                            </Layout>
                        </ProtectedRoute>
                    } />
                    
                    {/* Catch all - redirect to home */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </AuthProvider>
        </Router>
    )
}

export default App
