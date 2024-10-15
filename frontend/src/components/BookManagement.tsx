import React, { useState, useEffect } from 'react'
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"
import { fetchBooks, createBook, updateBook, deleteBook } from '../services/api'

interface Book {
  id: string
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
  const [bookForm, setBookForm] = useState<Omit<Book, 'id'>>({ isbn: '', title: '', authors: '', publisher: '', stock: 0 })
  const [editingBookId, setEditingBookId] = useState<string | null>(null)
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
  }, [currentPage, limit, setTotalBooks])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setBookForm(prev => ({ ...prev, [name]: name === 'stock' ? parseInt(value) : value }))
  }

  const resetForm = () => {
    setBookForm({ isbn: '', title: '', authors: '', publisher: '', stock: 0 })
    setEditingBookId(null)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (editingBookId) {
      updateBook(editingBookId, bookForm)
        .then(response => {
          setBooks(books.map(book => book.id === editingBookId ? { ...response.data, id: editingBookId } : book))
          resetForm()
          setError(null)
        })
        .catch(err => setError('Failed to update book'))
    } else {
      createBook(bookForm)
        .then(response => {
          setBooks([...books, response.data])
          setTotalBooks(prevTotal => prevTotal + 1)
          resetForm()
          setError(null)
        })
        .catch(err => setError('Failed to add book'))
    }
  }

  const handleEdit = (book: Book) => {
    setBookForm({ isbn: book.isbn, title: book.title, authors: book.authors, publisher: book.publisher, stock: book.stock })
    setEditingBookId(book.id)
  }

  const handleDelete = (id: string) => {
    deleteBook(id)
      .then(() => {
        setBooks(books.filter(book => book.id !== id))
        setTotalBooks(prevTotal => prevTotal - 1)
        setError(null)
      })
      .catch(err => setError('Failed to delete book'))
  }

  const totalPages = Math.ceil(totalBooks / limit)

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Book Management</h2>
      <p className="mb-4">Total Books: {totalBooks}</p>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="mb-4 grid grid-cols-6 gap-4">
        <Input
          placeholder="ISBN"
          name="isbn"
          value={bookForm.isbn}
          onChange={handleInputChange}
        />
        <Input
          placeholder="Title"
          name="title"
          value={bookForm.title}
          onChange={handleInputChange}
        />
        <Input
          placeholder="Author"
          name="authors"
          value={bookForm.authors}
          onChange={handleInputChange}
        />
        <Input
          placeholder="Publisher"
          name="publisher"
          value={bookForm.publisher}
          onChange={handleInputChange}
        />
        <Input
          type="number"
          placeholder="Stock"
          name="stock"
          value={bookForm.stock}
          onChange={handleInputChange}
        />
        <Button type="submit">{editingBookId ? 'Update Book' : 'Add Book'}</Button>
      </form>
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
          {books.map((book) => (
            <TableRow key={book.id}>
              <TableCell className="font-medium">{book.isbn}</TableCell>
              <TableCell>{book.title}</TableCell>
              <TableCell>{book.authors}</TableCell>
              <TableCell>{book.stock}</TableCell>
              <TableCell>
                <Button variant="outline" className="mr-2" onClick={() => handleEdit(book)}>Edit</Button>
                <Button variant="destructive" onClick={() => handleDelete(book.id)}>Delete</Button>
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