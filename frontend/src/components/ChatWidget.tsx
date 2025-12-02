import { useState } from 'react'
import { MessageSquare, X, Send } from 'lucide-react'

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState<{ text: string, isUser: boolean }[]>([
        { text: "Hello! How can I help you today?", isUser: false }
    ])
    const [input, setInput] = useState("")

    const handleSend = async () => {
        if (!input.trim()) return
        const userMessage = input
        setMessages([...messages, { text: userMessage, isUser: true }])
        setInput("")

        // Add loading message
        setMessages(prev => [...prev, { text: "Processing your request...", isUser: false }])

        try {
            // Call the backend chatbot API
            const response = await fetch('http://localhost:8000/api/chatbot/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
                },
                body: JSON.stringify({
                    message: userMessage,
                    user_email: localStorage.getItem('user_email') || 'guest@example.com'
                })
            })

            if (response.ok) {
                const data = await response.json()
                // Replace loading message with actual response
                setMessages(prev => prev.slice(0, -1).concat({ text: data.response, isUser: false }))
            } else {
                setMessages(prev => prev.slice(0, -1).concat({
                    text: "Sorry, I couldn't process your request. Please try again.",
                    isUser: false
                }))
            }
        } catch (error) {
            console.error('Chat error:', error)
            setMessages(prev => prev.slice(0, -1).concat({
                text: "Sorry, I'm having trouble connecting to the AI agents. Please ensure the backend is running.",
                isUser: false
            }))
        }
    }

    return (
        <div className="fixed bottom-4 right-4 z-50">
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-full p-4 shadow-lg transition-all"
                >
                    <MessageSquare className="h-6 w-6" />
                </button>
            )}

            {isOpen && (
                <div className="bg-white rounded-lg shadow-xl w-80 h-96 flex flex-col border border-gray-200">
                    <div className="bg-indigo-600 text-white p-4 rounded-t-lg flex justify-between items-center">
                        <h3 className="font-medium">AI Assistant</h3>
                        <button onClick={() => setIsOpen(false)} className="hover:text-gray-200">
                            <X className="h-5 w-5" />
                        </button>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] rounded-lg p-3 ${msg.isUser ? 'bg-indigo-100 text-indigo-900' : 'bg-gray-100 text-gray-900'}`}>
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="p-4 border-t border-gray-200">
                        <div className="flex space-x-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                                placeholder="Type a message..."
                                className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            />
                            <button
                                onClick={handleSend}
                                className="bg-indigo-600 text-white p-2 rounded-md hover:bg-indigo-700"
                            >
                                <Send className="h-5 w-5" />
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default ChatWidget
