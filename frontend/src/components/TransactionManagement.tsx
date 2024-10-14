import React, { useState, useEffect } from 'react'
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"
import { fetchTransactions, createTransaction, updateTransaction } from '../services/api'

interface Transaction {
  id: number
  bookId: number
  memberId: number
  issueDate: string
  returnDate: string | null
  rentFee: number
}

export function TransactionManagement() {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [newTransaction, setNewTransaction] = useState<Omit<Transaction, 'id' | 'returnDate' | 'rentFee'>>({ bookId: 0, memberId: 0, issueDate: '' })
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTransactions()
      .then(response => setTransactions(response.data))
      .catch(err => setError('Failed to fetch transactions'))
  }, [])

  const issueBook = () => {
    if (newTransaction.bookId && newTransaction.memberId && newTransaction.issueDate) {
      createTransaction(newTransaction)
        .then(response => {
          setTransactions([...transactions, response.data])
          setNewTransaction({ bookId: 0, memberId: 0, issueDate: '' })
        })
        .catch(err => setError('Failed to issue book'))
    }
  }

  const returnBook = (id: number) => {
    const transaction = transactions.find(t => t.id === id)
    if (transaction) {
      const returnDate = new Date().toISOString().split('T')[0]
      const daysRented = Math.ceil((new Date(returnDate).getTime() - new Date(transaction.issueDate).getTime()) / (1000 * 3600 * 24))
      const rentFee = daysRented * 10 // Assuming Rs. 10 per day
      updateTransaction(id, { ...transaction, returnDate, rentFee })
        .then(response => {
          setTransactions(transactions.map(t => t.id === id ? response.data : t))
        })
        .catch(err => setError('Failed to return book'))
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Transaction Management</h2>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="mb-4 flex gap-4">
        <Select onValueChange={(value: string) => setNewTransaction({...newTransaction, bookId: parseInt(value)})}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select Book" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="1">To Kill a Mockingbird</SelectItem>
            <SelectItem value="2">1984</SelectItem>
          </SelectContent>
        </Select>
        <Select onValueChange={(value: string) => setNewTransaction({...newTransaction, memberId: parseInt(value)})}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select Member" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="1">John Doe</SelectItem>
            <SelectItem value="2">Jane Smith</SelectItem>
          </SelectContent>
        </Select>
        <Input
          type="date"
          value={newTransaction.issueDate}
          onChange={(e) => setNewTransaction({...newTransaction, issueDate: e.target.value})}
        />
        <Button onClick={issueBook}>Issue Book</Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Book ID</TableHead>
            <TableHead>Member ID</TableHead>
            <TableHead>Issue Date</TableHead>
            <TableHead>Return Date</TableHead>
            <TableHead>Rent Fee</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {transactions.map((transaction) => (
            <TableRow key={transaction.id}>
              <TableCell>{transaction.bookId}</TableCell>
              <TableCell>{transaction.memberId}</TableCell>
              <TableCell>{transaction.issueDate}</TableCell>
              <TableCell>{transaction.returnDate || 'Not returned'}</TableCell>
              <TableCell>Rs. {transaction.rentFee}</TableCell>
              <TableCell>
                {!transaction.returnDate && (
                  <Button variant="outline" onClick={() => returnBook(transaction.id)}>Return Book</Button>
                )}
              </TableCell>
            </TableRow>

          ))}
        </TableBody>
      </Table>
    </div>
  )
}