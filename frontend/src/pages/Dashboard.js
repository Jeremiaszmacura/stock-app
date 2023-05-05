import { useContext, useState } from 'react';

import BaseCard from '../components/ui/BaseCard'
import styles from './Dashboard.module.css'
import { TokenContext, UserContext, AdminContext } from "../UserContext";

const DashboardPage = () => {

    let userInStorage = JSON.parse(localStorage.getItem('userInStorage'));

    const [newName, setNewName] = useState(null);
    const [newSurname, setNewSurname] = useState(null);
    const [newUsername, setNewUsername] = useState(null);

    const updateUser = (event) => {
        console.log("hi")
    }

    return (
        <div className={styles.dashboardPage}>
            <BaseCard>
            <div className={styles.accountDetails}>
            <h1>Account Details</h1>
                <div className={styles.customInputSection}>
                    <div className={styles.customInput}>
                        <label htmlFor='varHistoricalDays'>Name</label>
                        <input type='text' defaultValue={userInStorage.name} onChange={e => setNewName(e.target.value)} required id='varHistoricalDays' />
                    </div>
                    <div className={styles.customInput}>
                        <label htmlFor='varHorizonDays'>Surname</label>
                        <input type='text' defaultValue={userInStorage.surname} onChange={e => setNewSurname(e.target.value)} required id='varHorizonDays' />
                    </div>
                    <div className={styles.customInput}>
                        <label htmlFor='varHorizonDays'>Email</label>
                        <input id={styles.emailInput} type='text' defaultValue={userInStorage.username} onChange={e => setNewUsername(e.target.value)} required />
                    </div>
                </div>
                <div id={styles.selectButtonAdd}>
                    <button onClick={updateUser}>Update</button>
                </div>  
            </div>
            </BaseCard>
            <BaseCard>
                <h1>Analysis History</h1>
            </BaseCard>
        </div>
    );
}

export default DashboardPage;