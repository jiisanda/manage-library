import React, { useState } from 'react'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  children: React.ReactNode
  onValueChange?: (value: string) => void
}

export const Select: React.FC<SelectProps> = ({ children, onValueChange, ...props }) => {
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    if (onValueChange) {
      onValueChange(event.target.value)
    }
  }

  return (
    <select
      className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      onChange={handleChange}
      {...props}
    >
      {children}
    </select>
  )
}

export const SelectTrigger: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div className="relative" {...props}>{children}</div>
)

interface SelectValueProps extends React.HTMLAttributes<HTMLSpanElement> {
  placeholder?: string
}

export const SelectValue: React.FC<SelectValueProps> = ({ children, placeholder, ...props }) => (
  <span className="block truncate" {...props}>{children || placeholder}</span>
)

export const SelectContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div className="absolute mt-1 w-full rounded-md bg-white shadow-lg" {...props}>{children}</div>
)

export const SelectItem: React.FC<React.OptionHTMLAttributes<HTMLOptionElement>> = ({ children, ...props }) => (
  <option className="cursor-default select-none relative py-2 pl-3 pr-9" {...props}>{children}</option>
)