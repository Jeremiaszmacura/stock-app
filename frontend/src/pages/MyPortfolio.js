import { useState } from 'react';

import BaseCard from '../components/ui/BaseCard'
import PortfolioInvest from '../components/stock/PortfolioInvest'
import styles from './MyPortfolio.module.css'
import LoadingSpinner from "../components/ui/LoadingSpinner";


const MyPortfolioPage = () => {

    const defaultVarHistoricalDays = 200
    const defaultVarHorizonDays = 1
    const defaultPortflolioValue = 0
    const defaultConfidenceLevel = 99
    const defaultDateFrom = "2017-11-17"
    const defaultDateTo = "2018-11-16"

    const [companyInvestList, setCompanyInvestList] = useState([]);
    const [companyInvestSymbol, setCompanyInvestSymbol] = useState('');
    const [companyInvestValue, setCompanyInvestValue] = useState('');
    const [valueAtRisk, setValueAtRisk] = useState('');
    const [varType, setVarType] = useState('');
    const [varHorizonDays, setVarHorizonDays] = useState(defaultVarHorizonDays);
    const [portfolioAnalyseData, setPortfolioAnalyseData] = useState('');
    const [companyResultVar, setCompanyResultVar] = useState('');
    const [varHistoricalDays, setVarHistoricalDays] = useState(defaultVarHistoricalDays);
    const [varConfidenceLevel, setVarConfidenceLevel] = useState(defaultConfidenceLevel);
    const [isLoading, setIsLoading] = useState(false);
    const [dateFrom, setDateFrom] = useState(defaultDateFrom)
    const [dateTo, setDateTo] = useState(defaultDateTo)

    const addToPortfolio = (event) => {
        console.log("hi")
        let companyAdded = {
            symbol: companyInvestSymbol,
            value: Number(companyInvestValue)
        }
        setCompanyInvestList(companyInvestList => [...companyInvestList, companyAdded])
        console.log(companyInvestList)
    }

    const deleteHandler = () => {

    }

    const calculatePortfolioVaR = (event) => {
        setIsLoading(true)
        setCompanyResultVar(null);
        let protfolioVarData = {
            portfolio: companyInvestList,
            var_type: String(varType),
            horizon_days: Number(varHorizonDays),
            confidence_level: Number(varConfidenceLevel/100),
            date_from: String(dateFrom),
            date_to: String(dateTo),
        }
        console.log("fetch start")
        fetch(
            'http://localhost:8000/stock-data/portfolio-var/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " + localStorage.getItem('tokenInStorage'),
                },
                body: JSON.stringify(protfolioVarData)
            }
        )
        .then(res => {
            if (res.ok) {
                console.log('[CLIENT] fetch successful');
            } else {
                console.log('[CLIENT] fetch NOT successful');
            }
            res.json().then((data) => {
                data = JSON.parse(data)
                setIsLoading(false);
                setCompanyResultVar(data['var'].toFixed(2));
                setVarHistoricalDays(data['historical_days']);
                setPortfolioAnalyseData(data);
            });
        }).catch(err => {
            console.log(err);
            setIsLoading(false);
        });
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
                            <label htmlFor='varHistoricalDays'>Value to invest</label>
                            <input type='number' min="1" max="1000000000" onChange={e => setCompanyInvestValue(e.target.value)} required id='varHistoricalDays' />
                        </div>
                        <div id={styles.selectButtonAdd}>
                            <button onClick={addToPortfolio}>Add</button>
                        </div>
                    </div>
                </BaseCard>
                <BaseCard>
                    <div>
                        {companyInvestList.length > 0 &&
                            <div className={styles.investmentsBox}>
                                {companyInvestList.map((company, id) => (
                                    <PortfolioInvest
                                    key={id}
                                    companySymbol={company.companyInvestSymbol}
                                    companyValue={company.companyInvestValue}
                                    companyInvestList
                                    setCompanyInvestList
                                    />
                                ))}
                            </div>
                        }
                        {companyInvestList.length == 0 &&
                            <p id={styles.emptyPortfolio}>Portfolio empty</p>
                        }
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
                        </select>
                    </div>
                    </div>
                    <div className={styles.customInputSection}>
                        <div className={styles.dateInput}>
                            <div className={styles.dateInputUnit}>
                                <label htmlFor='varHistoricalDays'>Date from</label>
                                <input type="date" id="start" name="date-begin" min="1900-01-02" defaultValue={defaultDateFrom} onChange={e => setDateFrom(e.target.value)}/>
                            </div>
                            <div className={styles.dateInputUnit}>
                                <label htmlFor='varHistoricalDays'>Date to</label>
                                <input type="date" id="start" name="date-end" min="1900-01-01" defaultValue={defaultDateTo} onChange={e => setDateTo(e.target.value)}/>
                            </div>
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>VaR horizon in days</label>
                            <input type='number' min="10" max="10000" defaultValue={defaultVarHorizonDays} onChange={e => setVarHorizonDays(e.target.value)} required id='varHorizonDays' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>Confidence level %</label>
                            <input type='number' min="1" max="99" defaultValue={defaultConfidenceLevel} onChange={e => setVarConfidenceLevel(e.target.value)} required id='varConfidenceLevel' />
                        </div>
                    </div>
                    <div id={styles.selectButton}>
                        <button onClick={calculatePortfolioVaR}>Calculate</button>
                    </div>
                </BaseCard>
                {companyResultVar &&
                    <div className={styles.varResult}>
                        <BaseCard>
                            <div className={styles.varResultParameters}>
                                <p>VaR method:</p>
                                <p>Confidence level:</p>
                                <p>Historical days:</p>
                                <p>Time horizon:</p>
                                <p>{varType}</p>
                                <p>{varConfidenceLevel}%</p>
                                <p>{varHistoricalDays}</p>
                                <p>{varHorizonDays} days</p>
                            </div>
                            <p id={styles.varValue}> Value at Risk: {companyResultVar} </p>
                        </BaseCard>
                    </div>
                }
                { isLoading && <LoadingSpinner /> }
            </div>
        </div>
    );
}

export default MyPortfolioPage;
