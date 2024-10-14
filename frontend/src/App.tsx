import React, { useState, useEffect } from 'react'
import { BookManagement } from './components/BookManagement'
import { MemberManagement } from './components/MemberManagement'
import { TransactionManagement } from './components/TransactionManagement'
import { SearchComponent } from './components/SearchComponent'
import { BookOpen, Users, RefreshCw, Search } from 'lucide-react'
import { fetchBooks } from './services/api'

function App() {
  const [activeTab, setActiveTab] = useState('books')
  const [totalBooks, setTotalBooks] = useState(0)

  useEffect(() => {
    fetchBooks(1, 0)  // Fetch just one book to get the total count
      .then(response => {
        setTotalBooks(response.data.no_of_books)
      })
      .catch(err => console.error('Failed to fetch total book count', err))
  }, [])

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-md">
        <div className="p-4">
          <h1 className="text-2xl font-bold text-gray-800">Library Management</h1>
        </div>
        <nav className="mt-4">
          <button
            className={`w-full text-left px-4 py-2 flex items-center justify-between ${activeTab === 'books' ? 'bg-gray-200' : ''}`}
            onClick={() => setActiveTab('books')}
          >
            <div className="flex items-center">
              <BookOpen className="mr-2 h-5 w-5" />
              Books
            </div>
            <span className="bg-gray-300 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
              {totalBooks}
            </span>
          </button>
          <button
            className={`w-full text-left px-4 py-2 flex items-center ${activeTab === 'members' ? 'bg-gray-200' : ''}`}
            onClick={() => setActiveTab('members')}
          >
            <Users className="mr-2 h-5 w-5" />
            Members
          </button>
          <button
            className={`w-full text-left px-4 py-2 flex items-center ${activeTab === 'transactions' ? 'bg-gray-200' : ''}`}
            onClick={() => setActiveTab('transactions')}
          >
            <RefreshCw className="mr-2 h-5 w-5" />
            Transactions
          </button>
          <button
            className={`w-full text-left px-4 py-2 flex items-center ${activeTab === 'search' ? 'bg-gray-200' : ''}`}
            onClick={() => setActiveTab('search')}
          >
            <Search className="mr-2 h-5 w-5" />
            Search
          </button>
        </nav>
      </div>

      {/* Main content area */}
      <div className="flex-1 p-8 overflow-auto">
        {activeTab === 'books' && <BookManagement totalBooks={totalBooks} setTotalBooks={setTotalBooks} />}
        {activeTab === 'members' && <MemberManagement />}
        {activeTab === 'transactions' && <TransactionManagement />}
        {activeTab === 'search' && <SearchComponent />}
      </div>
    </div>
  )
}

export default App