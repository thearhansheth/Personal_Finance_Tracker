import { useUser } from '@clerk/clerk-react'
import { FinancialRecord } from './financial-form';
import { FinancialList } from './financial-list';

export const Dashboard = () =>{
    const { user } = useUser();
    return(
        <div className="dashboard-container">
            <h1>Welcome {user?.firstName}</h1>
            <FinancialRecord/>
            <FinancialList/>
        </div>
    )
}