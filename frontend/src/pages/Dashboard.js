import { useEffect, useState } from 'react';
import jwt from 'jwt-decode'

import BaseCard from '../components/ui/BaseCard'
import AnalysesHistory from '../components/users/AnalysesHistory';
import styles from './Dashboard.module.css'
import { TokenContext, UserContext, AdminContext } from "../UserContext";

const DashboardPage = () => {

    let userInStorage = JSON.parse(localStorage.getItem('userInStorage'));

    const [newName, setNewName] = useState(null);
    const [newSurname, setNewSurname] = useState(null);
    const [newUsername, setNewUsername] = useState(null);
    const [userAnalysisData, setUserAnalysisData] = useState([]);
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
                // console.log("1")
                // console.log(data["analysis_history"])
                // let result = []
                data = data["analysis_history"]
                // data = JSON.stringify(data["analysis_history"]);
                // let result = Object.keys(data).map((key) => [key, data[key]]);
                // for(var i in data)
                //     result.push([i, data[i]]);
                console.log("########################")
                console.log(typeof(data))
                console.log(data)
                setUserAnalysisData(data);
            });
        }).catch(err => {
            console.log(err);
        });
    }, [])

    const updateUser = (event) => {
        console.log(userInStorage.id)
        let updateUserData = {};
        if(userInStorage.name !== newName) {
            updateUserData["name"] = newName
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
                <h1 id={styles.analysisHistoryTitle}>Analysis History</h1>
                {/* {userAnalysisData} */}
                {/* {userAnalysisData && userAnalysisData.length > 0 && <p>hi</p>} */}
                {userAnalysisData && userAnalysisData.length > 0 && <AnalysesHistory analysesHistoryData={userAnalysisData}/>}
            </BaseCard>
        </div>
    );
}

export default DashboardPage;
