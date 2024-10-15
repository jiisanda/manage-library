import axios from "axios";

const API_BASE_URL = 'http://127.0.0.1:8000/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchBooks = (limit: number, offset: number) => api.get(`/books?limit=${limit}&offset=${offset}`);
export const createBook = (book: any) => api.post('/books', book);
export const updateBook = (id: string, book: any) => api.put(`/books/${id}`, book);
export const deleteBook = (id: string) => api.delete(`/books/${id}`);
export const searchBooks = (query: string) => api.get(`/books/search?q=${query}`);

export const fetchMembers = () => api.get('/members');
export const createMember = (member: any) => api.post('/members', member);
export const updateMember = (id: number, member: any) => api.put(`/members/${id}`, member);
export const deleteMember = (id: number) => api.delete(`/members/${id}`);

export const fetchTransactions = () => api.get('/transactions');
export const createTransaction = (transaction: any) => api.post('/transactions', transaction);
export const updateTransaction = (id: number, transaction: any) => api.put(`/transactions/${id}`, transaction);
export const deleteTransaction = (id: number) => api.delete(`/transactions/${id}`);

export default api;