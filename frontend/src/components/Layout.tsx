import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, ShoppingBag, Package, Users, BarChart2, LogOut, RotateCcw, Building2 } from 'lucide-react'

const Layout = ({ children }: { children: React.ReactNode }) => {
    const location = useLocation()

    const navigation = [
        { name: 'Dashboard', href: '/', icon: LayoutDashboard },
        { name: 'Purchase Orders', href: '/orders', icon: ShoppingBag },
        { name: 'Inventory', href: '/inventory', icon: Package },
        { name: 'Returns & RMA', href: '/returns', icon: RotateCcw },
        { name: 'Departments', href: '/customers', icon: Building2 },
        { name: 'Analytics', href: '/analytics', icon: BarChart2 },
    ]

    return (
        <div className="min-h-screen bg-slate-50 flex">
            {/* Sidebar */}
            <div className="hidden md:flex md:w-64 md:flex-col fixed inset-y-0 z-50">
                <div className="flex-1 flex flex-col min-h-0 bg-slate-900 shadow-xl">
                    <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
                        <div className="flex items-center flex-shrink-0 px-4 mb-8">
                            <div className="h-10 w-10 bg-indigo-500 rounded-lg flex items-center justify-center mr-3">
                                <Building2 className="h-6 w-6 text-white" />
                            </div>
                            <div>
                                <h1 className="text-white font-bold text-lg tracking-tight">Enterprise</h1>
                                <p className="text-slate-400 text-xs">Procurement Portal</p>
                            </div>
                        </div>
                        <nav className="mt-5 flex-1 px-2 space-y-1">
                            {navigation.map((item) => {
                                const isActive = location.pathname === item.href
                                return (
                                    <Link
                                        key={item.name}
                                        to={item.href}
                                        className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all duration-200 ${isActive
                                            ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30'
                                            : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                            }`}
                                    >
                                        <item.icon
                                            className={`mr-3 flex-shrink-0 h-5 w-5 transition-colors duration-200 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-white'
                                                }`}
                                            aria-hidden="true"
                                        />
                                        {item.name}
                                    </Link>
                                )
                            })}
                        </nav>
                    </div>
                    <div className="flex-shrink-0 flex border-t border-slate-800 p-4">
                        <div className="flex items-center w-full">
                            <div className="h-9 w-9 rounded-full bg-slate-700 flex items-center justify-center">
                                <span className="text-white font-semibold text-sm">PM</span>
                            </div>
                            <div className="ml-3 flex-1">
                                <p className="text-sm font-medium text-white">Procurement Manager</p>
                                <p className="text-xs font-medium text-slate-400">Admin Access</p>
                            </div>
                            <LogOut className="ml-auto h-5 w-5 text-slate-400 hover:text-white cursor-pointer" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Main content */}
            <div className="md:pl-64 flex flex-col flex-1">
                <main className="flex-1">
                    <div className="py-6">
                        <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
                            {children}
                        </div>
                    </div>
                </main>
            </div>
        </div>
    )
}

export default Layout
