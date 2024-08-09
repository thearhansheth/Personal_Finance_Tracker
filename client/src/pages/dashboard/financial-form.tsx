import { useState } from "react"
import { useUser } from '@clerk/clerk-react'

export const FinancialRecord = () => {

    const { user } = useUser();

    const [date, setDate] = useState<string>("")
    const [description, setDescription] = useState<string>("")
    const [amount, setAmount] = useState<string>("")
    const [category, setCategory] = useState<string>("")
    const [paymentMethod, setMethod] = useState<string>("")

    const handleSubmit = (event:React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const newRecord = () => {
            userID: user?.id
            date: date
            description: description
            amount: parseFloat(amount)
            category: category
            paymentMethod: paymentMethod
        };

        //addRecord(newRecord)
        setDate("")
        setDescription("")
        setAmount("")
        setCategory("")
        setMethod("")
    };

    return(
        <div className="form-container">
            <form onSubmit={handleSubmit}>
                <div className="form-field">
                    <label>Date:</label>
                    <input type="date" required className="input" value={date} onChange={(e) => setDate(e.target.value)}/>
                </div>
                <div className="form-field">
                    <label>Description:</label>
                    <input type="text" required className="input" value={description} onChange={(e) => setDescription(e.target.value)}/>
                </div>
                <div className="form-field">
                    <label>Amount:</label>
                    <input type="number" required className="input" value={amount} onChange={(e) => setAmount(e.target.value)}/>
                </div>
                <div className="form-field">
                    <label>Category:</label>
                    <select required className="input" value={category} onChange={(e) => setCategory(e.target.value)}>
                        <option value="">Select Category</option>
                        <option value="Food">Food</option>
                        <option value="Rent">Rent</option>
                        <option value="Income">Income</option>
                        <option value="Entertaiement">Entertainment</option>
                        <option value="Utilities">Utilities</option>
                        <option value="Shopping">Shopping</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div className="form-field">
                    <label>Payment Method:</label>
                    <select required className="input" value={paymentMethod} onChange={(e) => setMethod(e.target.value)}>
                        <option value="">Select Payment Method</option>
                        <option value="card">Credit/Debit Card</option>
                        <option value="cash">Cash</option>
                        <option value="bank-transfer">Bank Transfer</option>
                    </select>
                </div>
                <button type="submit" className="submitButton">Add Transaction</button>
            </form>
        </div>
    )
}