import React, { useState, useEffect } from 'react'
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"
import { fetchMembers, createMember, updateMember, deleteMember } from '../services/api'

interface Member {
  id: number
  name: string
  email: string
  outstandingDebt: number
}

export function MemberManagement() {
  const [members, setMembers] = useState<Member[]>([])
  const [newMember, setNewMember] = useState<Omit<Member, 'id'>>({ name: '', email: '', outstandingDebt: 0 })
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchMembers()
      .then(response => setMembers(response.data))
      .catch(err => setError('Failed to fetch members'))
  }, [])

  const addMember = () => {
    createMember(newMember)
      .then(response => {
        setMembers([...members, response.data])
        setNewMember({ name: '', email: '', outstandingDebt: 0 })
      })
      .catch(err => setError('Failed to add member'))
  }

  const deleteMemberHandler = (id: number) => {
    deleteMember(id)
      .then(() => {
        setMembers(members.filter(member => member.id !== id))
      })
      .catch(err => setError('Failed to delete member'))
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Member Management</h2>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="mb-4 flex gap-4">
        <Input
          placeholder="Name"
          value={newMember.name}
          onChange={(e) => setNewMember({...newMember, name: e.target.value})}
        />
        <Input
          placeholder="Email"
          value={newMember.email}
          onChange={(e) => setNewMember({...newMember, email: e.target.value})}
        />
        <Input
          type="number"
          placeholder="Outstanding Debt"
          value={newMember.outstandingDebt}
          onChange={(e) => setNewMember({...newMember, outstandingDebt: parseInt(e.target.value)})}
        />
        <Button onClick={addMember}>Add Member</Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Outstanding Debt</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {members.map((member) => (
            <TableRow key={member.id}>
              <TableCell>{member.name}</TableCell>
              <TableCell>{member.email}</TableCell>
              <TableCell>Rs. {member.outstandingDebt}</TableCell>
              <TableCell>
                <Button variant="outline" className="mr-2">Edit</Button>
                <Button variant="destructive" onClick={() => deleteMemberHandler(member.id)}>Delete</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}