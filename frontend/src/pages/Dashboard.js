import { useEffect, useState } from 'react';
import jwt from 'jwt-decode'

import BaseCard from '../components/ui/BaseCard'
import styles from './Dashboard.module.css'
import { TokenContext, UserContext, AdminContext } from "../UserContext";

const DashboardPage = () => {

    let userInStorage = JSON.parse(localStorage.getItem('userInStorage'));

    const [newName, setNewName] = useState(null);
    const [newSurname, setNewSurname] = useState(null);
    const [newUsername, setNewUsername] = useState(null);
    const [userData, setUserData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
            console.log(userInStorage.username)
        fetch(
            encodeURI(`http://localhost:8000/users/by-email/${userInStorage.username}`),
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            }
        )
        .then(res => {
            if (res.ok) {
                console.log('[CLIENT] fetch successful');
            } else {
                console.log(res);
            }
            res.json().then((data) => {
                data = JSON.stringify(data);
                setUserData(data);
            });
        }).catch(err => {
            console.log(err);
        });
    })

    const updateUser = (event) => {
        console.log(userInStorage.id)
        let updateUserData = {};
        if(userInStorage.name !== newName) {
            updateUserData["name"] = newName
        }
        if(userInStorage.surname !== newName) {
            updateUserData["surname"] = newSurname
        }
        if(userInStorage.username !== newName) {
            updateUserData["username"] = newUsername
        }
        if(Object.keys(updateUserData).length) {
            setIsLoading(true);
            fetch(
                `http://localhost:8000/users/${userInStorage.id}`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updateUserData)
                }
            )
            .then(res => {
                if (res.ok) {
                    console.log('[CLIENT] fetch successful');
                } else {
                    console.log(res);
                }
                res.json().then((data) => {
                    const token = data.access_token;
                    const userData = jwt(token)
                    localStorage.setItem('tokenInStorage', token);
                    localStorage.setItem('userInStorage', JSON.stringify(userData));
                    data = JSON.stringify(data)
                    console.log(data)
                    setIsLoading(false);
                });
            }).catch(err => {
                console.log(err);
                setIsLoading(false);
            });
        }
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