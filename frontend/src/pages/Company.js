import { useState } from 'react';
import { useLocation } from 'react-router-dom';

import BaseCard from '../components/ui/BaseCard'
import styles from './Company.module.css'


const CompanyPage = () => {

    const { state } = useLocation();
    const { symbol, name, type, region, marketOpen, marketClose, timezone, currency, matchScore } = state;
    const [companyResult, setCompanyResult] = useState('');
    const [selectedInterval, setSelectedInterval] = useState('');
    const [valueAtRisk, setValueAtRisk] = useState('');
    const [hurstExponent, setHurstExponent] = useState('');

    const selectInterval = (event) => {
        setSelectedInterval(event.target.value)
    }

    const intervalSearchHandler = (event) => {
        event.preventDefault();
        if (!selectedInterval) {
            return
        }
        const CompanySearchData = {
            symbol: symbol,
            interval: selectedInterval,
            calculate: [valueAtRisk, hurstExponent]
        }
        fetch(
            'http://localhost:8000/stock-data/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(CompanySearchData)
            }
        )
        .then(res => {
            if (res.ok) {
                console.log('[CLIENT] login - fetch successful');
            } else {
                console.log('[CLIENT] login - fetch NOT successful');
            }
            res.json().then((data) => {
                setCompanyResult(data); 
            });
        }).catch(err => {
            console.log(err);
        });
    }

    return (
        <div className={styles.companyPage}>
            <div className={styles.overBaseCard}>
                <BaseCard>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Symbol:</p>
                        <p className={styles.pVariable}>{symbol}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Name:</p>
                        <p className={styles.pVariable}>{name}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Type:</p>
                        <p className={styles.pVariable}>{type}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Region:</p>
                        <p className={styles.pVariable}>{region}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Market Open:</p>
                        <p className={styles.pVariable}>{marketOpen}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Market Close:</p>
                        <p className={styles.pVariable}>{marketClose}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Timezone:</p>
                        <p className={styles.pVariable}>{timezone}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Currency:</p>
                        <p className={styles.pVariable}>{currency}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Match Score:</p>
                        <p className={styles.pVariable}>{matchScore}</p>
                    </div>
                </BaseCard>
            </div>

            <div className={styles.analyzeCompany}>
                <div className={styles.customSelect}>
                    <select onChange={selectInterval} defaultValue={''}>
                        <option hidden value="" disabled>Time Interval</option>
                        <option value="1min">1min</option>
                        <option value="5min">5min</option>
                        <option value="15min">15min</option>
                        <option value="30min">30min</option>
                        <option value="60min">60min</option>
                        <option value="daily">daily</option>
                        <option value="weekly">weekly</option>
                        <option value="monthly">monthly</option>
                    </select>
                    <button onClick={intervalSearchHandler}>Select</button>
                </div>

                <div className={styles.multiSelect}>
                    <div className={styles.multiSelectBox}>
                        <form>
                            <input onChange={e => setValueAtRisk(e.target.value)} type="checkbox" id="var" name="var" value="var"/>
                            <label htmlFor="var">Value at Risk</label>
                            <input onChange={e => setHurstExponent(e.target.value)} type="checkbox" id="hurst" name="hurst" value="hurst"/>
                            <label htmlFor="hurst">Hurst Exponent</label>
                        </form>
                    </div>
                </div>
            </div>
            
                {companyResult && 
                    <div className={styles.plot}>
                        <div className={styles.plotBox}>
                            <img src={`data:image/png;base64,${companyResult}`} alt='Plot'/>
                        </div>
                    </div>
                }
        </div>
        
    );
}

export default CompanyPage;