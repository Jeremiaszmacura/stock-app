import { useState } from 'react';

import BaseCard from '../components/ui/BaseCard'
import styles from './MyPortfolio.module.css'


const MyPortfolioPage = () => {

    const defaultVarHistoricalDays = 200
    const defaultVarHorizonDays = 1
    const defaultPortfloioValue = 1000
    const defaultConfidenceLevel = 99

    const [companyInvestSymbol, setCompanyInvestSymbol] = useState('');
    const [companyInvestValue, setCompanyInvestValue] = useState('');
    const [valueAtRisk, setValueAtRisk] = useState('');
    const [varType, setVarType] = useState('');
    const [varHistoricalDays, setVarHistoricalDays] = useState(defaultVarHistoricalDays);
    const [varHorizonDays, setVarHorizonDays] = useState(defaultVarHorizonDays);
    const [varPortfloioValue, setVarPortfloioValue] = useState(defaultPortfloioValue);
    const [varConfidenceLevel, setVarConfidenceLevel] = useState(defaultConfidenceLevel);

    const addToPortfolio = (event) => {
        console.log("hi")
    }

    return (
        <div className="home-page">
            <div className={styles.invest}>
                <BaseCard>
                    <div className={styles.investBox}>
                        <div className={styles.customInput}>
                            <label htmlFor='varHistoricalDays'>Company Symbol</label>
                            <input type='text' onChange={e => setCompanyInvestSymbol(e.target.value)} required id='varHistoricalDays' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHistoricalDays'>Portfolio value</label>
                            <input type='number' min="1" max="1000000000" onChange={e => setCompanyInvestValue(e.target.value)} required id='varHistoricalDays' />
                        </div>
                        <div id={styles.selectButtonAdd}>
                            <button onClick={addToPortfolio}>Add</button>
                        </div>  
                    </div>
                </BaseCard>
                <BaseCard>
                <div className={styles.investmentsBox}>
                        <p id={styles.emptyPortfolio}>Portfolio empty</p>
                    </div> 
                </BaseCard>
            </div>
            <div className={styles.portfolioVar}>
                <BaseCard>
                    <div className={styles.portfolioVarFirst}>
                        <p>Value at Risk for my portfolio</p>
                        <div className={styles.customSelect}>
                        <select onChange={e => setVarType(e.target.value)} defaultValue={''}>
                            <option hidden value="" disabled>VaR type</option>
                            <option value="historical">historical simulation</option>
                            <option value="linear_model">linear model simulation</option>
                            <option value="monte_carlo">monte carlo simulation</option>
                        </select>
                    </div>
                    </div>
                    <div className={styles.customInputSection}>
                        <div className={styles.customInput}>
                            <label htmlFor='varHistoricalDays'>VaR historical days</label>
                            <input type='number' min="10" max="10000" defaultValue={defaultVarHistoricalDays} onChange={e => setVarHistoricalDays(e.target.value)} required id='varHistoricalDays' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>VaR horizon in days</label>
                            <input type='number' min="10" max="10000" defaultValue={defaultVarHorizonDays} onChange={e => setVarHorizonDays(e.target.value)} required id='varHorizonDays' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>Portfolio value</label>
                            <input type='number' min="10" max="1000000000" defaultValue={defaultPortfloioValue} onChange={e => setVarPortfloioValue(e.target.value)} required id='varPortfloioValue' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>Confidence level %</label>
                            <input type='number' min="1" max="99" defaultValue={defaultConfidenceLevel} onChange={e => setVarConfidenceLevel(e.target.value)} required id='varConfidenceLevel' />
                        </div>
                    </div>
                    <div id={styles.selectButton}>
                        <button onClick={addToPortfolio}>Calculate</button>
                    </div>  
                </BaseCard>
            </div>  
        </div>
    );
}

export default MyPortfolioPage;