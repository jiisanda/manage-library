import React, { useState } from 'react'
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"
import { searchBooks } from '../services/api'

interface Book {
  id: number
  title: string
  author: string
  stock: number
}

export function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('')
  const [searchResults, setSearchResults] = useState<Book[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleSearch = () => {
    searchBooks(searchTerm)
      .then(response => {
        setSearchResults(response.data)
        setError(null)
      })
      .catch(err => {
        setError('Failed to search books')
        setSearchResults([])
      })
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Search Books</h2>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="mb-4 flex gap-4">
        <Input
          placeholder="Search by book name or author"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button onClick={handleSearch}>Search</Button>
      </div>
      {searchResults.length > 0 && (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Title</TableHead>
              <TableHead>Author</TableHead>
              <TableHead>Stock</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {searchResults.map((book) => (
              <TableRow key={book.id}>
                <TableCell>{book.title}</TableCell>
                <TableCell>{book.author}</TableCell>
                <TableCell>{book.stock}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  )
}