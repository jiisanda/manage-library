import React, { useState, useEffect } from 'react'
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"
import { fetchBooks, createBook, updateBook, deleteBook } from '../services/api'

interface Book {
  id: number
  title: string
  authors: string
  stock: number
  isbn: string
  publisher: string
}

interface BookManagementProps {
  totalBooks: number
  setTotalBooks: React.Dispatch<React.SetStateAction<number>>
}

export function BookManagement({ totalBooks, setTotalBooks }: BookManagementProps) {
  const [books, setBooks] = useState<Book[]>([])
  const [newBook, setNewBook] = useState<Omit<Book, 'id'>>({ isbn: '', title: '', authors: '', publisher: '', stock: 0 })
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [limit] = useState(10)

  useEffect(() => {
    fetchBooks(limit, (currentPage - 1) * limit)
      .then(response => {
        setBooks(response.data.result)
        setTotalBooks(response.data.no_of_books)
      })
      .catch(err => setError('Failed to fetch books'))
  }, [currentPage, limit])

  const addBook = () => {
    createBook(newBook)
      .then(response => {
        setBooks([...books, response.data])
        setNewBook({isbn: '', title: '', authors: '', publisher: '', stock: 0 })
        setTotalBooks(prevTotal => prevTotal + 1)
      })
      .catch(err => setError('Failed to add book'))
  }

  const deleteBookHandler = (id: number) => {
    deleteBook(id)
      .then(() => {
        setBooks(books.filter(book => book.id !== id))
        setTotalBooks(prevTotal => prevTotal - 1)
      })
      .catch(err => setError('Failed to delete book'))
  }

  const totalPages = Math.ceil(totalBooks / limit)

  const truncateText = (text: string, maxLength: number) => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Book Management</h2>
      <p className="mb-4">Total Books: {totalBooks}</p>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="mb-4 flex gap-4">
        <Input
          placeholder="ISBN"
          value={newBook.isbn}
          onChange={(e) => setNewBook({...newBook, isbn: e.target.value})}
        />
        <Input
          placeholder="Title"
          value={newBook.title}
          onChange={(e) => setNewBook({...newBook, title: e.target.value})}
        />
        <Input
          placeholder="Author"
          value={newBook.authors}
          onChange={(e) => setNewBook({...newBook, authors: e.target.value})}
        />
        <Input
          placeholder="Publisher"
          value={newBook.publisher}
          onChange={(e) => setNewBook({...newBook, publisher: e.target.value})}
        />
        <Input
          type="number"
          placeholder="Stock"
          value={newBook.stock}
          onChange={(e) => setNewBook({...newBook, stock: parseInt(e.target.value)})}
        />
        <Button onClick={addBook}>Add Book</Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[150px]">ISBN</TableHead>
            <TableHead className="w-[300px]">Title</TableHead>
            <TableHead className="w-[250px]">Authors</TableHead>
            <TableHead className="w-[100px]">Stock</TableHead>
            <TableHead className="w-[200px]">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {books.map((book, index) => (
            <TableRow key={index}>
              <TableCell className="font-medium">{book.isbn}</TableCell>
              <TableCell title={book.title}>{truncateText(book.title, 40)}</TableCell>
              <TableCell title={book.authors}>{truncateText(book.authors, 30)}</TableCell>
              <TableCell>{book.stock}</TableCell>
              <TableCell>
                <Button variant="outline" className="mr-2">Edit</Button>
                <Button variant="destructive" onClick={() => deleteBookHandler(book.id)}>Delete</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className="mt-4 flex justify-between items-center">
        <Button
          onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
        >
          Previous
        </Button>
        <span>Page {currentPage} of {totalPages}</span>
        <Button
          onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
          disabled={currentPage === totalPages}
        >
          Next
        </Button>
      </div>
    </div>
  )
}