import { Package, ShoppingBag, Users, AlertCircle } from 'lucide-react'

// --- Types ---
export interface Order {
    id: number
    customer_id: number
    customer_name: string
    status: 'DELIVERED' | 'PROCESSING' | 'SHIPPED' | 'PENDING' | 'CANCELLED'
    total_amount: number
    created_at: string
    items: number
}

export interface InventoryItem {
    id: number
    name: string
    sku: string
    stock: number
    price: number
    status: 'In Stock' | 'Low Stock' | 'Out of Stock' | 'Critical'
    category: string
}

export interface Customer {
    id: number
    name: string
    email: string
    phone: string
    location: string
    status: 'Active' | 'Inactive' | 'Blocked'
    lastOrder: string
    totalSpent: number
}

// --- Data ---

export const customers: Customer[] = [
    { id: 1, name: 'Alice Johnson', email: 'alice@example.com', phone: '+1 (555) 123-4567', location: 'New York, NY', status: 'Active', lastOrder: '2023-10-24', totalSpent: 1250.50 },
    { id: 2, name: 'Bob Smith', email: 'bob@example.com', phone: '+1 (555) 987-6543', location: 'San Francisco, CA', status: 'Active', lastOrder: '2023-10-20', totalSpent: 850.00 },
    { id: 3, name: 'Charlie Brown', email: 'charlie@example.com', phone: '+1 (555) 456-7890', location: 'Austin, TX', status: 'Inactive', lastOrder: '2023-09-15', totalSpent: 120.00 },
    { id: 4, name: 'Diana Prince', email: 'diana@example.com', phone: '+1 (555) 222-3333', location: 'Chicago, IL', status: 'Active', lastOrder: '2023-10-25', totalSpent: 3400.00 },
    { id: 5, name: 'Evan Wright', email: 'evan@example.com', phone: '+1 (555) 444-5555', location: 'Seattle, WA', status: 'Active', lastOrder: '2023-10-22', totalSpent: 560.00 },
    { id: 6, name: 'Fiona Gallagher', email: 'fiona@example.com', phone: '+1 (555) 666-7777', location: 'Boston, MA', status: 'Blocked', lastOrder: '2023-08-10', totalSpent: 0.00 },
    { id: 7, name: 'George Martin', email: 'george@example.com', phone: '+1 (555) 888-9999', location: 'Denver, CO', status: 'Active', lastOrder: '2023-10-18', totalSpent: 900.00 },
    { id: 8, name: 'Hannah Montana', email: 'hannah@example.com', phone: '+1 (555) 000-1111', location: 'Los Angeles, CA', status: 'Active', lastOrder: '2023-10-26', totalSpent: 2100.00 },
]

export const inventory: InventoryItem[] = [
    { id: 1, name: 'Wireless Headphones', sku: 'WH-001', stock: 45, price: 129.99, status: 'In Stock', category: 'Electronics' },
    { id: 2, name: 'Ergonomic Office Chair', sku: 'EC-042', stock: 12, price: 249.50, status: 'Low Stock', category: 'Furniture' },
    { id: 3, name: 'Mechanical Keyboard', sku: 'MK-108', stock: 8, price: 89.99, status: 'Low Stock', category: 'Electronics' },
    { id: 4, name: 'USB-C Docking Station', sku: 'DS-007', stock: 150, price: 75.00, status: 'In Stock', category: 'Accessories' },
    { id: 5, name: '27" 4K Monitor', sku: 'MN-400', stock: 0, price: 399.99, status: 'Out of Stock', category: 'Electronics' },
    { id: 6, name: 'Laptop Stand', sku: 'LS-022', stock: 65, price: 29.99, status: 'In Stock', category: 'Accessories' },
    { id: 7, name: 'Noise Cancelling Earbuds', sku: 'NE-099', stock: 32, price: 149.99, status: 'In Stock', category: 'Electronics' },
    { id: 8, name: 'Smart Watch Series 5', sku: 'SW-005', stock: 3, price: 299.00, status: 'Critical', category: 'Wearables' },
]

export const orders: Order[] = [
    { id: 1001, customer_id: 1, customer_name: 'Alice Johnson', status: 'DELIVERED', total_amount: 129.99, created_at: '2023-10-24T10:00:00Z', items: 1 },
    { id: 1002, customer_id: 2, customer_name: 'Bob Smith', status: 'PROCESSING', total_amount: 499.00, created_at: '2023-10-26T14:30:00Z', items: 2 },
    { id: 1003, customer_id: 4, customer_name: 'Diana Prince', status: 'PENDING', total_amount: 75.00, created_at: '2023-10-27T09:15:00Z', items: 1 },
    { id: 1004, customer_id: 8, customer_name: 'Hannah Montana', status: 'SHIPPED', total_amount: 299.00, created_at: '2023-10-26T11:20:00Z', items: 1 },
    { id: 1005, customer_id: 5, customer_name: 'Evan Wright', status: 'DELIVERED', total_amount: 149.99, created_at: '2023-10-22T16:45:00Z', items: 1 },
    { id: 1006, customer_id: 1, customer_name: 'Alice Johnson', status: 'PROCESSING', total_amount: 89.99, created_at: '2023-10-27T10:00:00Z', items: 1 },
]

// --- Derived Statistics ---

export const stats = {
    totalOrders: orders.length,
    totalRevenue: orders.reduce((sum, order) => sum + order.total_amount, 0),
    pendingShipments: orders.filter(o => o.status === 'PROCESSING' || o.status === 'PENDING').length,
    openTickets: 5, // Mock value
    totalCustomers: customers.length,
    activeCustomers: customers.filter(c => c.status === 'Active').length,
    lowStockItems: inventory.filter(i => i.status === 'Low Stock' || i.status === 'Critical').length,
}

export const revenueData = [
    { label: 'Mon', revenue: 450, cost: 300 },
    { label: 'Tue', revenue: 650, cost: 400 },
    { label: 'Wed', revenue: 450, cost: 250 },
    { label: 'Thu', revenue: 800, cost: 500 },
    { label: 'Fri', revenue: 550, cost: 350 },
    { label: 'Sat', revenue: 900, cost: 600 },
    { label: 'Sun', revenue: 700, cost: 450 },
]

export const growthData = [
    { label: 'Jan', value: 30 },
    { label: 'Feb', value: 45 },
    { label: 'Mar', value: 35 },
    { label: 'Apr', value: 60 },
    { label: 'May', value: 55 },
    { label: 'Jun', value: 85 },
    { label: 'Jul', value: 75 },
]
